from django.db import models
from timescale.db.models.models import TimescaleModel


# Create your models here.

class PointerPositionEvent(TimescaleModel):
    browser = models.ForeignKey("dashboard.Browser", on_delete=models.CASCADE)
    x = models.IntegerField("X", default=0)
    y = models.IntegerField("Y", default=0)

    class Meta:
        verbose_name = "Position Event"
        verbose_name_plural = "Position Events"
        app_label = 'analytics'
        db_table = 'pointer_position_event'

    def __str__(self):
        return "@" + str(self.time) + " (" + str(self.x) + ", " + str(self.y) + ")"
