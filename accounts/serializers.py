from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'name', 'password', 'role']

    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            role=validated_data.get('role', 'user'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
