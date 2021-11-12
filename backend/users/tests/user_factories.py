import factory
from factory.fuzzy import FuzzyText
from users.models import Activationtoken, User


class UserDictFactory(factory.DictFactory):
    email = factory.Sequence(lambda n: f"user{n + 1}@gmail.com")
    password = FuzzyText(length=8)


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n + 1}@gmail.com")
    password = FuzzyText(length=8)


class UserTokenFactory(factory.Factory):
    class Meta:
        model = Activationtoken
