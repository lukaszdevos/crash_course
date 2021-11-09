from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
