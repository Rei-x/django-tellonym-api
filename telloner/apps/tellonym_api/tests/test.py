from django.test import TestCase
from django.urls import reverse
from .credentials import test_credentials
import time


class LoginTest(TestCase):
    def test_login_good_credentials(self):
        response = self.client.post(reverse('tellonym_api:login'), test_credentials)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auth")

    def test_login_bad_credentials(self):
        bad_credentials = {'username': 'username',
                           'password': 'password'}
        response = self.client.post(reverse('tellonym_api:login'), bad_credentials)
        self.assertEqual(response.status_code, 401)

    def tearDown(self):
        time.sleep(1)

class ListTest(TestCase):
    def test_no_post_data(self):
        response = self.client.post(reverse('tellonym_api:index'))
        self.assertEqual(response.status_code, 401)
