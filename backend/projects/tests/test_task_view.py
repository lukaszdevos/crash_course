from unittest import TestCase

import pytest
from projects.project_factories import (ProjectDictFactory, ProjectFactory,
                                        TaskDictFactory)
from rest_framework import status
from rest_framework.test import APIClient
from users.tests.user_factories import UserFactory

pytestmark = pytest.mark.django_db


class TestTask(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.given_created_user()
        self.project = self.given_created_project()
        self.client.force_authenticate(user=self.user)

    def given_created_project(self):
        project = ProjectFactory(created_by=self.user)
        project.save()
        return project

    def given_created_user(self):
        user = UserFactory(is_active=True)
        user.save()
        return user

    def given_get_response_endpoint(self, url):
        self.response = self.client.get(url)

    def given_update_response_endpoint(self, url, data):
        self.response = self.client.patch(url, data)

    def given_post_response_endpoint(self, url, data):
        self.response = self.client.post(url, data)

    def test_task_create(self):
        self._given_task_has_been_created()

        self._then_task_will_be_created()

    def test_task_create(self):
        self._given_task_has_been_created()

        self._then_task_will_be_created()

    def test_task_list_belong_to_project(self):
        number_project = 2
        self._given_task_has_been_created(number_project)

        self._given_project_tasks_list()

        self.assertEqual(len(self.response.json()), number_project)

    def test_task_list_not_belong_to_project(self):
        project_id = self.project.id
        self._given_task_has_been_created_related_to_another_project()

        url = f"/projects/{project_id}/tasks/"
        self.given_get_response_endpoint(url)

        expected_num_project = 0
        self.assertEqual(len(self.response.json()), expected_num_project)

    def test_task_update_view(self):
        self._given_task_has_been_created()
        task_id = self.response.json()["id"]
        data = {"title": "new_title"}

        url = f"/projects/{self.project.id}/tasks/{task_id}/"
        self.given_update_response_endpoint(url, data)

        self.assertEqual(self.response.json()["title"], data["title"])
        # self.assertEqual(self.response.json()["description"], data["description"])


    def _given_project_tasks_list(self):
        url = f"/projects/{self.project.id}/tasks/"
        self.given_get_response_endpoint(url)

    def _given_task_has_been_created_related_to_another_project(self):
        another_project = ProjectFactory(created_by=self.user)
        another_project.save()
        self.project = another_project
        self._given_task_has_been_created()

    def _given_task_has_been_created(self, number=1):
        self.data = TaskDictFactory.build_batch(number, project=self.project.id)
        url = f"/projects/{self.project.id}/tasks/"
        for i in range(number):
            self.given_post_response_endpoint(url, self.data[i])

    def _then_task_will_be_created(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.json()["title"], self.data[0]["title"])
        self.assertEqual(
            self.response.json()["description"], self.data[0]["description"]
        )
        self.assertEqual(self.response.json()["status"], self.data[0]["status"])
