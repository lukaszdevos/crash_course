from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Activationtoken, TokenException
from users.serializers import UserLoginSerializer, UserSerializer


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


class UserActivateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if token := request.GET.get("token"):
            try:
                Activationtoken.objects.activate(token=token)
                return Response({"message": "Account confirmed."})
            except TokenException as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})


class UserLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
