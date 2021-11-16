from unittest import TestCase

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from users.tests.user_factories import UserDictFactory, UserFactory

pytestmark = pytest.mark.django_db


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_login = {"email": "test@gmail.com", "password": "password_secret"}
        self._given_user_has_been_created(**self.data_login)

    def test_user_login(self):
        self._then_user_log_in(self.data_login)

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.response.json()["refresh"])
        self.assertTrue(self.response.json()["access"])

    def test_user_login_with_incorrect_password(self):
        self._then_user_log_in_with_invalid_data()

        expected_result = {"detail": "Invalid username or password"}
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.response.json(), expected_result)

    def _then_user_log_in_with_invalid_data(self):
        invalid_data_login = {"email": "test@gmail.com", "password": "invalid_password"}
        self._then_user_log_in(invalid_data_login)

    def _then_user_log_in(self, data_login):
        url = "/users/login/"
        self.given_post_response_endpoint(url, data_login)

    def _given_activate_user_account(self):
        self.user.is_active = True
        self.user.save()

    def _given_user_has_been_created(self, **kwargs):
        self.user = UserFactory.build(is_active=True, **kwargs)
        self.user.save()
        self.user = User.objects.get(email=self.response.json()["email"])

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

    def given_post_response_endpoint_with_empty_data(self, url):
        self.response = self.client.post(url)
