from analytics.models import PointerPositionEvent
from common.serializer.base import BaseSerializer


class PointerPositionEventSerializer(BaseSerializer):

    class Meta:
        model = PointerPositionEvent

        fields = (
            "id",
            "time",
            "browser",
            "x",
            "y",
        )

        read_only_fields = (
            "id",
            "browser",
        )
