from unittest import TestCase

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from users.tests.user_factories import UserDictFactory

pytestmark = pytest.mark.django_db


class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        self._given_user_has_been_created()

        self.assertEqual(self.response.status_code, 201)

    def _given_user_has_been_created(self):
        self.data = UserDictFactory.build()
        url = reverse("users:register")
        self.given_post_response_endpoint(url, self.data)

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)
