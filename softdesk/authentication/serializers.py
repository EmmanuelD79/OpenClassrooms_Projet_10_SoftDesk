from rest_framework import serializers
from authentication.models import User


class Userserializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email']
