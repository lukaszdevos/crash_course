from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import ActivationToken, TokenException, User
from users.serializers import UserLoginSerializer, UserSerializer, MemberSerializer


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer


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
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


class MembersListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = MemberSerializer

    def get_queryset(self):
        keyword = self.kwargs["keyword"]
        return self.queryset.filter(
            Q(email__contains=keyword) | Q(display_name__contains=keyword)
        )[:6]
