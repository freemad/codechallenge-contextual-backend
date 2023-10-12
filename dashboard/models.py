from django.db import models
from timescale.db.models.models import TimescaleModel

from common.utils import random_util

# Create your models here.
INSTANCE_ID_MAX_LENGTH = 64


def browser_instance():
    return random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)


class Browser(models.Model):
    instance_id = models.SlugField("Instance ID", max_length=INSTANCE_ID_MAX_LENGTH, default=browser_instance)
    is_active = models.BooleanField("Is Active", default=True)

    class Meta:
        verbose_name = "Browser"
        verbose_name_plural = "Browsers"
        app_label = 'dashboard'
        db_table = 'browser'

    def __str__(self):
        return "id: " + str(self.id) + " (" + ("active" if self.is_active else "inactive") + ")"


class PointerStatus(TimescaleModel):
    browser = models.ForeignKey("dashboard.Browser", on_delete=models.CASCADE)
    interval = models.IntegerField("Interval (ms)")
    avg_velocity = models.FloatField("Average Velocity")
    traversed_distance = models.FloatField("Traversed Distance")
    start_x = models.IntegerField("Start X")
    start_y = models.IntegerField("Start X")
    end_x = models.IntegerField("End X")
    end_y = models.IntegerField("End X")

    class Meta:
        verbose_name = "Pointer Status"
        verbose_name_plural = "Pointer Statuses"
        app_label = 'dashboard'
        db_table = 'pointer_status'

    def __str__(self):
        return "@" + str(self.time) + ": " + str(self.avg_velocity)

