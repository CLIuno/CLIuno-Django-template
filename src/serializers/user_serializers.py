from rest_framework import serializers

from src.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'date_of_birth',
            'gender', 'nationality', 'phone', 'email', 'is_online',
            'is_verified', 'is_otp_enabled', 'is_otp_verified',
            'is_deleted', 'role', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'nationality', 'phone',
        ]


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirmation = serializers.CharField(
        min_length=8, write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        return data


class LoginSerializer(serializers.Serializer):
    usernameOrEmail = serializers.CharField()
    password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    usernameOrEmail = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)
    password_confirmation = serializers.CharField(min_length=8, required=False)

    def validate(self, data):
        confirmation = data.get('password_confirmation')
        if confirmation is not None and data['password'] != confirmation:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'})
        return data


class ChangePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField()
    newPassword = serializers.CharField(min_length=8)
