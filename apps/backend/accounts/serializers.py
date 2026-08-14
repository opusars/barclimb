from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import User, normalize_email
from .validators import normalize_username


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "is_email_verified")
        read_only_fields = fields


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_email(self, value: str) -> str:
        value = normalize_email(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("An account already uses this email.")
        return value

    def validate_username(self, value: str) -> str:
        value = normalize_username(value)
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is unavailable.")
        return value

    def validate(self, attrs):
        candidate = User(email=attrs["email"], username=attrs["username"])
        try:
            password_validation.validate_password(attrs["password"], candidate)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": list(error.messages)}) from error
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)

    def validate_email(self, value: str) -> str:
        return normalize_email(value)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        return normalize_email(value)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(trim_whitespace=True, write_only=True, min_length=32)


class ResetPasswordSerializer(TokenSerializer):
    new_password = serializers.CharField(trim_whitespace=False, write_only=True)
