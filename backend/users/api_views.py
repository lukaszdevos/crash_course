from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from users.models import UserToken
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer


class UserLoginView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        if token:
            user_token = UserToken.objects.get(token=token)
            if user_token.is_valid_token():
                user = user_token.user
                user.is_active = True
                user.save()
                return Response({"message": "Account confirmed."})
            else:
                return Response({"message": "Token verification expired."})
        return Response({})
