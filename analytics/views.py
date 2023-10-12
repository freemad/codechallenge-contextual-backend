from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError

from analytics.models import PointerPositionEvent
from analytics.serializers import PointerPositionEventSerializer
from common import (web_keys, messages)
from dashboard.models import Browser


# Create your views here.

@api_view(["GET"])
def sync(request):
    return JsonResponse(
        {
            web_keys.SERVER_TIME: timezone.now(),
        },
        status=200
    )


@api_view(["GET"])
def event(request, instance_id, pk):
    event_obj = get_object_or_404(PointerPositionEvent, pk=pk, browser__instance_id=instance_id)

    return JsonResponse(
        {
            web_keys.EVENT: PointerPositionEventSerializer(event_obj).data,
        },
        status=200
    )


@api_view(["POST"])
def event_list(request, instance_id):
    browser = get_object_or_404(Browser, instance_id=instance_id)
    event_data_list = request.data
    if event_data_list is None or type(event_data_list) is not list:
        return JsonResponse(
            {web_keys.MESSAGE: messages.MSG_ERR_DATA_NOT_VALID},
            status=400
        )
    event_serializer_list = list()
    try:
        for event_data in event_data_list:
            event_serializer = PointerPositionEventSerializer(data=event_data)
            if event_serializer.is_valid(raise_exception=True):
                event_serializer_list.append(event_serializer)
    except ValidationError:
        return JsonResponse(
            {web_keys.MESSAGE: messages.MSG_ERR_DATA_NOT_VALID},
            status=400
        )

    for event_serializer in event_serializer_list:
        event_serializer.save(browser=browser)

    return JsonResponse(
        data={web_keys.MESSAGE: messages.MSG_OK_SUCCESSFUL},
        status=200
    )
