import factory
from factory.fuzzy import FuzzyText, FuzzyChoice

from projects.models import Project, Task


class ProjectDictFactory(factory.DictFactory):
    name = FuzzyText(length=20)


class ProjectFactory(factory.Factory):
    class Meta:
        model = Project

    name = FuzzyText(length=20)


class TaskDictFactory(factory.DictFactory):
    title = FuzzyText(length=20)
    description = FuzzyText(length=100)
    status = FuzzyChoice([Task.TO_DO])
