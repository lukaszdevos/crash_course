from unittest import TestCase

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from users.models import User
from users.tests.user_factories import UserDictFactory

pytestmark = pytest.mark.django_db


class UserTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_create(self):
        self._given_user_has_been_created()

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def _given_user_has_been_created(self, **kwargs):
        self.data = UserDictFactory.build(**kwargs)
        url = "/users/register/"
        self.given_post_response_endpoint(url, self.data)

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

    def test_user_not_create_when_has_not_valid_email(self):
        wrong_email = "wrong_mail.com"
        self._given_user_has_been_created(email=wrong_email)

        expected_result = ["Enter a valid email address."]

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.json()["email"], expected_result)

    def test_user_not_create_when_has_not_valid_password(self):
        short_password = "short"
        self._given_user_has_been_created(password=short_password)

        expected_result = [
            "This password is too short. It must contain at least 8 characters."
        ]

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.json()["password"], expected_result)

    def test_user_create_validation_error_when_has_no_password(self):
        short_password = ""
        self._given_user_has_been_created(password=short_password)

        expected_result = ["This field may not be blank."]

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.json()["password"], expected_result)

    def test_user_token_when_user_created(self):
        self._given_user_has_been_created()

        user = User.objects.get(email=self.response.json()["email"])

        self.assertTrue(user.token.first())
