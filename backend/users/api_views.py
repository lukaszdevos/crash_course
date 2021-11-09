from users.models import User
from rest_framework.generics import CreateAPIView
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
