from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import TokenException, UserToken
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer


class UserActivateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        if token := request.GET.get("token"):
            try:
                UserToken.objects.activate(token=token)
                return Response({"message": "Account confirmed."})
            except TokenException as e:
                return Response({"message": str(e)}, status=400)
        return Response({})
