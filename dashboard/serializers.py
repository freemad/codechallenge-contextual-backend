from common.serializer.base import BaseSerializer
from dashboard.models import Browser, PointerStatus


class BrowserSerializer(BaseSerializer):

    class Meta:
        model = Browser
        fields = (
            "id",
            "instance_id",
            "is_active",
        )

        read_only_fields = (
            "id",
        )


class PointerStatusSerializer(BaseSerializer):

    class Meta:
        model = PointerStatus

        fields = (
            'time',
            'browser',
            'interval',
            'avg_velocity',
            'traversed_distance',
            'start_x',
            'start_y',
            'end_x',
            'end_y',
        )
