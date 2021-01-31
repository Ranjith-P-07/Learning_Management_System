from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(min_length=4, max_length=15)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile_number', 'role', 'password',
                  'confirm_password']

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("This email is already exists..!!")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Password does not match...!!")
        data['password'] = make_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        user.is_active = False
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=10, required=True)
    password = serializers.CharField(max_length=15, required=True)


class EmailSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class ResetSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class ChangeUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=15, min_length=4)
    new_password = serializers.CharField(max_length=15, min_length=4)
    confirm_password = serializers.CharField(max_length=15, min_length=4)

    def validate(self, data):
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError("Password does not Match!")
        return data
