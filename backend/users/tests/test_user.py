from unittest import TestCase

from rest_framework.test import APIClient


class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        pass

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)
