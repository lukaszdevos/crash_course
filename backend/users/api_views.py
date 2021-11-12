from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import TokenError, UserToken
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer


class UserActivateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        token = request.GET.get("token")
        if token:
            try:
                UserToken.objects.activate(token=token)
                return Response({"message": "Account confirmed."})
            except TokenError as e:
                return Response({"message": str(e)}, status=400)
        return Response({})
