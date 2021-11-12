from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from users.models import TokenException, Activationtoken
from users.serializers import UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer


class UserActivateView(CreateAPIView):
    def post(self, request, *args, **kwargs):
        if token := request.GET.get("token"):
            try:
                Activationtoken.objects.activate(token=token)
                return Response({"message": "Account confirmed."})
            except TokenException as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})
