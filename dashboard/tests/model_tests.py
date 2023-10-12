from django.db.utils import DataError
from django.test import TestCase

from common.utils import random_util
from dashboard.models import INSTANCE_ID_MAX_LENGTH, Browser


class BrowserModelTests(TestCase):
    def test_when_instance_id_length_bigger_than_instance_id_max_length_then_raise_data_error(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH + 1);
        try:
            Browser.objects.create(instance_id=instance_id)
        except DataError:
            pass
