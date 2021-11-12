import datetime

import pytest
from django.utils import timezone
from users.tests.user_factories import UserFactory, UserTokenFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def user():
    user = UserFactory.build()
    return user


def test_user_token_is_valid(user):
    time_delta = timezone.now() - datetime.timedelta(hours=23)
    token = UserTokenFactory.build(user=user, created_at=time_delta)

    assert token.is_valid_token() == True


def test_user_token_is_invalid(user):
    time_delta = timezone.now() - datetime.timedelta(hours=48)
    token = UserTokenFactory.build(user=user, created_at=time_delta)

    assert token.is_valid_token() == False
