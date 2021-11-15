from unittest import TestCase

import pytest
from projects.project_factory import ProjectDictFactory
from rest_framework import status
from rest_framework.test import APIClient
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

    # def given_update_response_endpoint(self, url, data):
    #     self.response = self.client.patch(url, data)
    #
    # def given_delete_response_endpoint(self, url):
    #     self.response = self.client.delete(url)

    def given_created_user(self):
        user = UserFactory(is_active=True)
        user.save()
        return user

    def test_project_create(self):
        self._given_project_has_been_created()

        self._then_project_will_be_created()

    def test_user_project_list_view(self):
        number_project = 2
        self._given_project_has_been_created(number_project)
        self._given_project_created_by_another_user()

        self._given_user_projects_list()

        self.assertEqual(len(self.response.json()), number_project)

    def _given_project_created_by_another_user(self):
        another_user = UserFactory(is_active=True)
        another_user.save()
        another_user_client = APIClient()
        another_user_client.force_authenticate(user=another_user)
        another_user_project = ProjectDictFactory.build()
        url = "/projects/"
        self.response = another_user_client.post(url, another_user_project)

    def _given_user_projects_list(self):
        url = "/projects/"
        self.given_get_response_endpoint(url)

    def _given_project_has_been_created(self, number=1):
        self.data = ProjectDictFactory.build_batch(number)
        url = "/projects/"
        for i in range(number):
            self.given_post_response_endpoint(url, self.data[i])

    def _then_project_will_be_created(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.json()["name"], self.data[0]["name"])
        self.assertEqual(self.response.json()["member"], [])
