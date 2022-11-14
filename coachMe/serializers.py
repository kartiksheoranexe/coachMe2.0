from rest_framework_json_api import serializers
from coachMe.models import Coach, Package



class CoachListSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='user.first_name')

    class Meta:
        model = Coach
        fields = ['coach_name']


class PackageListSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach')

    class Meta:
        model = Package
        fields = ['coach_name','package_name', 'package_desc', 'duration_type','duration','base_price']