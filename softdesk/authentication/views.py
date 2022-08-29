from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import Userserializer


class UserViewset(ModelViewSet):

    serializer_class = Userserializer

    def get_queryset(self):
        return User.objects.all()

# Create your views here.
