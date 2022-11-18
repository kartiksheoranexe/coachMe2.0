"""coachMe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from knox import views as knox_views
from coachMe.views import CoachListAPIView, DisplayPackageAPIView, RegisterUserAPIView, LoginAPIView, PurchasePackageAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_user/', RegisterUserAPIView.as_view(), name = 'register'),
    path('login_user/', LoginAPIView.as_view(), name='login'),
    path('logout_user/', knox_views.LogoutView.as_view(), name='logout'),

    path('coach_me/coach_list/', CoachListAPIView.as_view()),
    path('coach_me/package_list/', DisplayPackageAPIView.as_view()),

    path('coach_me/purchase/', PurchasePackageAPIView.as_view())

]
