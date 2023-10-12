from datetime import timedelta

from celery import Celery, shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from analytics.models import PointerPositionEvent
from common.utils.math_util import (calculate_distance, calculate_velocity)
from core.settings import CHART_GRANULARITY
from dashboard.models import (Browser, PointerStatus)

app = Celery()

logger = get_task_logger(__name__)


@app.task
def active_browsers_event_handler():
    active_browsers = Browser.objects.filter(is_active=True)
    for active_browser in active_browsers:
        calculate_pointer_status.delay(active_browser.id, timezone.now())


@shared_task
def calculate_pointer_status(active_browser_id, at_datetime):
    ranges = (at_datetime - timedelta(seconds=CHART_GRANULARITY), at_datetime)
    events = PointerPositionEvent.timescale.filter(time__range=ranges, browser=active_browser_id).order_by("time")
    events = events.to_list()
    n = len(events)

    if n == 0:
        start_x = 0
        end_x = 0
        start_y = 0
        end_y = 0
    else:
        start_x = events[0].x
        start_y = events[0].y
        end_x = events[n - 1].x
        end_y = events[n - 1].y

    total_distance = 0
    # todo: suggestions
    for i in range(0, n - 1):
        start = events[i]
        end = events[i + 1]
        distance = calculate_distance(end, start)
        total_distance += distance
    avg_velocity = calculate_velocity(total_distance, (ranges[1].timestamp() - ranges[0].timestamp()))
    PointerStatus.objects.create(
        time=ranges[0] + (ranges[1] - ranges[0]) / 2,
        browser=Browser.objects.get(pk=active_browser_id),
        interval=(ranges[1].timestamp() - ranges[0].timestamp()) * 1000,  # in milliseconds
        avg_velocity=avg_velocity,
        traversed_distance=total_distance,
        start_x=start_x,
        start_y=start_y,
        end_x=end_x,
        end_y=end_y
    )
