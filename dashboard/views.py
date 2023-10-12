from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from common import (web_keys, messages)
from core.settings import (
    EVENT_GRANULARITY,
    EVENT_PER_BATCH_COUNT,
    CHART_GRANULARITY)
from dashboard.models import (
    Browser,
    PointerStatus)
from dashboard.serializers import (
    BrowserSerializer,
    PointerStatusSerializer)


# Create your views here.

@api_view(["GET"])
def logon(request):
    instance_id = request.query_params.get(web_keys.INSTANCE_ID)
    if instance_id is not None:
        browser = Browser.objects.filter(instance_id=instance_id).first()
        if browser is None:
            try:
                browser_serializer = BrowserSerializer(data={"instance_id": instance_id})
                browser_serializer.is_valid(raise_exception=True)
                browser_serializer.save()
                browser = Browser.objects.get(instance_id=instance_id)
            except ValidationError:
                return JsonResponse(
                    {web_keys.MESSAGE: messages.MSG_ERR_DATA_NOT_VALID},
                    status=400
                )
    else:
        browser = Browser.objects.create()

    browser.is_active = True
    browser.save()
    return JsonResponse(
        data={
            web_keys.BROWSER_ID: browser.id,
            web_keys.INSTANCE_ID: browser.instance_id,
            web_keys.EVENT_GRANULARITY: EVENT_GRANULARITY,
            web_keys.EVENT_PER_BATCH_COUNT: EVENT_PER_BATCH_COUNT,
            web_keys.CHART_GRANULARITY: CHART_GRANULARITY,
            web_keys.SERVER_TIME: timezone.now()
        },
        status=200
    )


@api_view(["GET"])
def logoff(request, instance_id):
    try:
        browser_serializer = BrowserSerializer(data={"instance_id": instance_id})
        browser_serializer.is_valid(raise_exception=True)
    except ValidationError:
        return JsonResponse(
            {web_keys.MESSAGE: messages.MSG_ERR_DATA_NOT_VALID},
            status=400
        )

    browser = get_object_or_404(Browser, instance_id=instance_id)
    browser.is_active = False
    browser.save()
    return JsonResponse(
        data={
            web_keys.MESSAGE: messages.MSG_OK_SUCCESSFUL
        },
        status=200
    )


@api_view(["GET"])
def pointer_statuses(request, instance_id):
    browser = get_object_or_404(Browser, instance_id=instance_id)

    timedelta_sec = request.query_params.get(web_keys.TIMEDELTA) \
        if request.query_params.get(web_keys.TIMEDELTA) is not None else CHART_GRANULARITY
    ranges = (timezone.now() - timedelta(seconds=int(timedelta_sec) + CHART_GRANULARITY),
              timezone.now() - timedelta(seconds=CHART_GRANULARITY))
    statuses = PointerStatus.timescale.filter(time__range=ranges, browser=browser)
    status_list = list()
    for status in statuses:
        status_list.append(PointerStatusSerializer(status).data)

    return JsonResponse(
        data={
            web_keys.STATUSES: status_list
        },
        status=200,
    )

