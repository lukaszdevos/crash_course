from unittest import TestCase

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from projects.project_factory import ProjectDictFactory
from users.tests.user_factories import UserFactory

pytestmark = pytest.mark.django_db


class TestProject(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.given_created_user()
        self.client.force_authenticate(user=self.user)

    def given_get_response_endpoint(self, url):
        self.response = self.client.get(url)

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

    def given_update_response_endpoint(self, url, data):
        self.response = self.client.patch(url, data)

    def given_delete_response_endpoint(self, url):
        self.response = self.client.delete(url)

    def given_created_user(self):
        user = UserFactory(is_active=True)
        user.save()
        return user

    def test_project_create(self, **kwargs):
        self._given_project_has_been_created(kwargs)

        self._then_project_will_be_created()

    def _given_project_has_been_created(self, kwargs):
        self.data = ProjectDictFactory.build(**kwargs)
        url = "/projects/"
        self.given_post_response_endpoint(url, self.data)

    def _then_project_will_be_created(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.json()["name"], self.data["name"])
        self.assertEqual(self.response.json()["member"], [])

