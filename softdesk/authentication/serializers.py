
from rest_framework import serializers
from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name']



class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user = User.objects.create_user(email=validated_data['email'], first_name=self.validated_data['first_name'], last_name=self.validated_data['last_name'], password=validated_data['password'])

        return user
