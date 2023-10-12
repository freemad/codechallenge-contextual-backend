from django.urls import reverse
from rest_framework.test import APITestCase

from common.utils import random_util
from dashboard.models import INSTANCE_ID_MAX_LENGTH, Browser


# def test_when_instance_id_and_pk_not_matched_then_404(self):
class EventViewTests(APITestCase):
    def test_get_logon_when_instance_id_invalid_then_400(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH + 1)
        url = "/dashboard/logon/?instance-id=" + instance_id
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_logon_when_browser_with_provided_instance_id_not_present_then_create(self):
        instance_id = random_util.generate_alphanumeric_uid(4)
        url = "/dashboard/logon/?instance-id=" + instance_id
        response = self.client.get(url, format='json')
        browser = Browser.objects.get(instance_id=instance_id)
        self.assertIsNotNone(browser)
        self.assertEqual(response.status_code, 200)

    def test_get_logon_when_no_instance_id_then_create(self):
        url = reverse("dashboard:logon")
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_logoff_when_instance_id_invalid_then_400(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH + 1)
        url = "/dashboard/" + instance_id + "/logoff/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_pointer_statuses_when_browser_with_instance_id_not_present_then_404(self):
        instance_id = random_util.generate_alphanumeric_uid(INSTANCE_ID_MAX_LENGTH)
        url = "dashboard/" + instance_id + "statuses/"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 404)

