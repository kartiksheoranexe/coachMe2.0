from django.shortcuts import render
from django.contrib.auth import login

from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from coachMe.models import Coach, Package
from coachMe.serializers import CoachListSerializer, PackageListSerializer, UserSerializer, RegisterUserSerializer


# Create your views here.
class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPIView(KnoxLoginView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid()
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)


class CoachListAPIView(generics.ListAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachListSerializer

class DisplayPackageAPIView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer
  

  
    
   
        



