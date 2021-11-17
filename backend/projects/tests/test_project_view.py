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

    def given_update_response_endpoint(self, url, data):
        self.response = self.client.patch(url, data)

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

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

    def test_user_project_list_view_when_user_is_member(self):
        self._given_project_created_by_another_user(member=[self.user.id])

        self._given_user_projects_list()

        user_belong_to_project = 1
        self.assertEqual(len(self.response.json()), user_belong_to_project)

    def test_user_project_list_view_when_user_is_not_member(self):
        self._given_project_created_by_another_user()

        self._given_user_projects_list()

        user_belong_to_project = 0
        self.assertEqual(len(self.response.json()), user_belong_to_project)

    def test_user_project_detail_view_when_user_is_member(self):
        self._given_project_created_by_another_user(member=[self.user.id])

        self._given_user_projects_detail()

        self.assertEqual(
            self.response.json()["name"], self.another_user_project["name"]
        )
        self.assertTrue(self.response.json()["created_by"])
        self.assertTrue(self.response.json()["created_at"])
        self.assertTrue(self.response.json()["member"])

    def test_user_project_detail_view_when_user_is_not_member(self):
        self._given_project_created_by_another_user()

        self._given_user_projects_detail()

        expected = {"detail": "Not found."}
        self.assertEqual(self.response.json(), expected)

    def test_user_project_detail_view_when_user_is_member(self):
        self._given_project_has_been_created()
        project_id = self.response.json()["id"]
        data = {"name": "new_name"}

        self._given_updated_project(data, project_id)

        self.assertEqual(self.response.json()["name"], data["name"])

    def _given_updated_project(self, data, project_id):
        url = f"/projects/{project_id}/"
        self.given_update_response_endpoint(url, data)

    def _given_project_created_by_another_user(self, **kwargs):
        self.another_user = UserFactory(is_active=True)
        self.another_user.save()
        another_user_client = APIClient()
        another_user_client.force_authenticate(user=self.another_user)
        self.another_user_project = ProjectDictFactory.build(**kwargs)
        url = "/projects/"
        self.response = another_user_client.post(url, self.another_user_project)

    def _given_user_projects_list(self):
        url = "/projects/"
        self.given_get_response_endpoint(url)

    def _given_user_projects_detail(self):
        id = self.another_user.created_by.first().id
        url = f"/projects/{id}/".format(id)
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
