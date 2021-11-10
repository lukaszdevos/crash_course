from unittest import TestCase
from django.urls import reverse
import pytest

from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        data = {"email": "test1234@test.com", "password": "test"}
        url = reverse("users:register")
        self.given_post_response_endpoint(url, data)
        self.assertEqual(self.response.status_code, 201)

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)
