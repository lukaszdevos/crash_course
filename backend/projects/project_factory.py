import factory
from factory.fuzzy import FuzzyText


class ProjectDictFactory(factory.DictFactory):
    name = FuzzyText(length=20)
