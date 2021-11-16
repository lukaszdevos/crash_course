from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.models import ActivationToken, TokenException
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import UserLoginSerializer, UserSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserActivateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if token := request.GET.get("token"):
            try:
                ActivationToken.objects.activate(token=token)
                return Response({"message": "Account confirmed."})
            except TokenException as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

