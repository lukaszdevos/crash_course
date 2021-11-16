from unittest import TestCase

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from users.tests.user_factories import UserFactory

pytestmark = pytest.mark.django_db


class MemberListView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.given_created_user()
        self.client.force_authenticate(user=self.user)

    def given_created_user(self):
        user = UserFactory(is_active=True, display_name="display_name")
        user.save()
        return user

    def given_get_response_endpoint(self, url):
        self.response = self.client.get(url)

    def test_search_user_should_not_return_user(self):
        keyword = "wired@email.com"
        self._given_user_list(keyword)

        self.assertEqual(self.response.json(), [])

    def test_search_user_by_email_should_return_user(self):
        keyword = "user"

        self._then_users_will_be_displayed(keyword)

    def test_search_user_by_display_name_should_return_user(self):
        keyword = "display"

        self._then_users_will_be_displayed(keyword)

    def test_search_user_by_email_should_return_user(self):
        keyword = "user"
        number_users = 10

        self._given_num_users_has_been_created(number_users)
        self._given_user_list(keyword)

        expected_users = 6
        self.assertEqual(len(self.response.json()), expected_users)


    def _then_users_will_be_displayed(self, keyword):
        self._given_user_list(keyword)
        self.assertEqual(self.response.json()[0]["id"], self.user.id)
        self.assertEqual(self.response.json()[0]["email"], self.user.email)
        self.assertEqual(self.response.json()[0]["display_name"], self.user.display_name)

    def _given_user_list(self, keyword):
        url = f"/users/search/{keyword}/"
        self.given_get_response_endpoint(url)

    def _given_num_users_has_been_created(self, number=1):
        users_list = UserFactory.build_batch(number)
        for user in users_list:
            user.save()
