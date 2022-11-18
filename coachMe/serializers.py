from coachMe.models import Coach, Package
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'dob', 'gender', 'phone_no', 'user_type')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name',
                  'last_name', 'dob', 'gender', 'phone_no', 'user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create_user(self, validated_data):
        user = User.objects.create(validated_data['username'], validated_data['email'], validated_data['password'], validated_data['first_name'],
                                   validated_data['last_name'], validated_data['dob'], validated_data['gender'], validated_data['user_type'])
        return user


class CoachListSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='user.first_name')

    class Meta:
        model = Coach
        fields = ['coach_name']


class PackageListSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach')

    class Meta:
        model = Package
        fields = ['coach_name', 'package_name', 'package_desc',
                  'duration_type', 'duration', 'base_price']
