import factory
from factory.fuzzy import FuzzyText


class UserDictFactory(factory.DictFactory):
    email = factory.Sequence(lambda n: f"user{n + 1}@gmail.com")
    password = FuzzyText(length=8)


