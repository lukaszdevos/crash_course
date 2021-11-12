import datetime
from unittest import TestCase

import pytest
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from users.tests.user_factories import UserDictFactory

pytestmark = pytest.mark.django_db


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def _given_user_has_been_created(self, **kwargs):
        self.data = UserDictFactory.build(**kwargs)
        url = "/users/register/"
        self.given_post_response_endpoint(url, self.data)
        self.user = User.objects.get(email=self.response.json()["email"])

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

    def given_post_response_endpoint_with_empty_data(self, url):
        self.response = self.client.post(url)

    def test_user_activate_when_token_not_expired(self):
        self._given_user_has_been_created()
        self._given_user_token()

        self._given_activate_page_with_token()

        expected_message = "Account confirmed."
        self.assertEqual(self.response.json()["message"], expected_message)

    def _given_activate_page_with_token(self):
        url = "/users/activate/" + "?token=" + self.user_token.token
        self.given_post_response_endpoint_with_empty_data(url)

    def test_user_activate_when_token_expired(self):
        self._given_user_has_been_created()
        self._given_user_token()

        self._change_token_date()
        self._given_activate_page_with_token()

        expected_message = "Token verification expired."
        self.assertEqual(self.response.json()["message"], expected_message)

    def _change_token_date(self):
        time_delta = timezone.now() - datetime.timedelta(hours=48)
        self.user_token.created_at = time_delta
        self.user_token.save()

    def _given_user_token(self):
        self.user_token = self.user.token.first()

    def test_user_activate_page(self):
        self._given_user_activate_page()

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def _given_user_activate_page(self):
        url = "/users/activate/"
        self.given_post_response_endpoint_with_empty_data(url)

    def test_user_activate_when_token_is_invalid(self):
        self._given_user_has_been_created()
        self._given_user_token()

        self._change_token_date()
        self._given_activate_page_with_invalid_token()

        expected_message = "Token verification is invalid."
        self.assertEqual(self.response.json()["message"], expected_message)

    def _given_activate_page_with_invalid_token(self):
        invalid_token = "this is invalid token"
        url = "/users/activate/" + "?token=" + invalid_token
        self.given_post_response_endpoint_with_empty_data(url)
