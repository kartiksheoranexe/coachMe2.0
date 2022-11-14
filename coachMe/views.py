from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from coachMe.models import Coach, Package
from coachMe.serializers import CoachListSerializer, PackageListSerializer
from rest_framework import generics

# Create your views here.


class CoachListAPIView(generics.ListAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachListSerializer

class DisplayPackageAPIView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
  

  
    
   
        



