from unittest import TestCase

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from users.tests.user_factories import UserDictFactory

pytestmark = pytest.mark.django_db


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_login(self):
        data_login = {"email": "test@gmail.com", "password": "password_secret"}
        self._given_user_has_been_created(**data_login)
        self._given_activate_user_account()

        self._then_user_log_in(data_login)

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_user_login_with_incorrect_password(self):
        data_login = {"email": "test@gmail.com", "password": "password_secret"}
        self._given_user_has_been_created(**data_login)
        self._given_activate_user_account()

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
        self.user_token = self.user.token.first()
        url = "/users/activate/" + "?token=" + self.user_token.token
        self.given_post_response_endpoint_with_empty_data(url)

    def _given_user_has_been_created(self, **kwargs):
        self.data = UserDictFactory.build(**kwargs)
        url = "/users/register/"
        self.given_post_response_endpoint(url, self.data)
        self.user = User.objects.get(email=self.response.json()["email"])

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

    def given_post_response_endpoint_with_empty_data(self, url):
        self.response = self.client.post(url)
