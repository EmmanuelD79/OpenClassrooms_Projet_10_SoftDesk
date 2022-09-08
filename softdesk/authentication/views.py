from authentication.models import User
from authentication.serializers import UserSerializer, SignupSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework import status, viewsets, response
from .utils import get_tokens_for_user
from rest_framework.permissions import AllowAny


class UserViewset(viewsets.ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class SignupView(viewsets.ViewSet):

    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer
    authentication_classes= []


    def create(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({
            'msg': 'User is created',
            'user': serializer.data,
        })


class LoginView(APIView):

    permission_classes = (AllowAny,)
    authentication_classes= []

    def post(self, request):
        if 'email' not in request.data or 'password' not in request.data:
            return response.Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            tokens = get_tokens_for_user(request.user)
            return response.Response({'msg': 'Login Success', **tokens}, status=status.HTTP_200_OK)
        return response.Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        