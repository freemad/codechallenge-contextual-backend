from django.utils import timezone
from rest_framework.test import APITestCase

from common.utils import random_util
from dashboard.models import INSTANCE_ID_MAX_LENGTH, Browser


class AnalyticsViewTests(APITestCase):
    def test_get_sync_always_200(self):
        url = "/analytics/sync/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_event_when_pk_and_instance_id_not_match_then_404(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        pk = 1
        url = "/analytics/" + instance_id + "/events/" + str(pk) + "/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_post_event_list_when_browser_not_present_then_404(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        url = "/analytics/" + instance_id + "/events/"
        data = [{"time": timezone.now(), "x": 0, "y": 0}]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_post_event_list_when_request_data_not_list_then_400(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        Browser.objects.create(instance_id=instance_id)
        url = "/analytics/" + instance_id + "/events/"
        data = {"time": timezone.now(), "x": 0, "y": 0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_event_list_when_request_data_not_present_then_400(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        Browser.objects.create(instance_id=instance_id)
        url = "/analytics/" + instance_id + "/events/"
        response = self.client.post(url, None, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_event_list_when_request_data_not_valid_then_400(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        Browser.objects.create(instance_id=instance_id)
        url = "/analytics/" + instance_id + "/events/"
        data = [{"some-data": "some data"}]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_event_list_when_request_data_ok_then_200(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        Browser.objects.create(instance_id=instance_id)
        url = "/analytics/" + instance_id + "/events/"
        data = [{"time": timezone.now(), "x": 0, "y": 0}]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

