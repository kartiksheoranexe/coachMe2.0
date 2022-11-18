from django.shortcuts import render
from django.contrib.auth import login

import requests
import uuid

from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from coachMe.models import Coach, Package, User, Client, Mapping, Transaction
from coachMe.serializers import CoachListSerializer, PackageListSerializer, UserSerializer, RegisterUserSerializer
from coachMe.wrappers import welcome

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


class PurchasePackageAPIView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        welcome()
        current_user = self.request.user
        print("Welcome !  " + current_user.first_name)
        if (current_user.user_type == 'U') or (current_user.user_type == 'L'):
            url = 'http://127.0.0.1:8000/coach_me/coach_list/'
            data = {}
            coach_api_call = requests.get(url, headers={}, data=data)

            while True:
                print("Coache's available: ")
                coach_list = coach_api_call.json()
                for select_coach in coach_list:
                    print(select_coach['coach_name'])
                print("Select a coach : ")
                user_input = input()
                for select_coach in coach_list:
                    found = 0
                    if user_input == select_coach['coach_name']:
                        found = 1
                        user_obj = User.objects.filter(
                            first_name=user_input)[0]
                        user_id = user_obj.id
                        coach_obj = Coach.objects.get(user=user_id)
                        packages = Package.objects.filter(coach_id=coach_obj)

                        print("Package's Avaiable : ")
                        for i in packages:
                            pkg_id = i.id
                            amount_paid = i.base_price
                            pckg_name = i.package_name
                            print("Package id : " + str(pkg_id))
                            print("Name : " + i.package_name)
                            print("Package Description : " + i.package_desc)
                            print(
                                "Duration Type (Year, Month, Days) : " + i.duration_type)
                            print("Package Duration : " + str(i.duration))
                            print("Price : " + str(amount_paid))

                        user_package_input = int(input("Choose package id: "))

                        def confirmation(user_package_input):
                            found = 0
                            for i in packages:
                                pkg_id = i.id
                                purchase_amount = i.base_price
                                package_obj = Package.objects.filter(id=i.id).first()
                                if user_package_input == pkg_id:
                                    found = 1
                                    print(user_package_input)
                                    print("Amount to be paid : ",
                                          int(purchase_amount))
                                    print(
                                        "Type Yes to confirm or No to return to the coach list")
                                    confirmation = input()
                                    if confirmation == "YES" or confirmation == "yes":
                                        client, created = Client.objects.update_or_create(
                                            user=current_user, coach=coach_obj)

                                        u_id = uuid.uuid4()  # for Transaction objects creating while purchasing
                                        transaction, created = Transaction.objects.get_or_create(
                                            unique_id=u_id, amount_paid=purchase_amount, status='P', mode='ND', remark='Purchase Succesfull', type='P', client=client)
                                        mapping, created = Mapping.objects.get_or_create(
                                            package_id=package_obj, coach_id=coach_obj, price=purchase_amount, client=client
                                        )
                                        print("Select Mode :  ")
                                        print(
                                            "Press 1 for Credit Card, 2 for Debit Card, 3 for UPI) :")
                                        payment_confirm = int(input())
                                        if payment_confirm == 1 or 2 or 3:
                                            if payment_confirm == 1:
                                                transaction.status = 'S'
                                                transaction.mode = 'CC'
                                                transaction.save()
                                            elif payment_confirm == 2:
                                                transaction.status = 'S'
                                                transaction.mode = 'DC'
                                                transaction.save()
                                            else:
                                                transaction.status = 'S'
                                                transaction.mode = 'UPI'
                                                transaction.save()
                                        else:
                                            print("Enter correct mode number.")

                                        current_user.user_type = 'L'
                                        current_user.save()
                                    
                                        print({"Coach Hired!": "Success!", "Coach": coach_obj.user.first_name,  "Client": current_user.first_name, "Package": pckg_name, "Price": amount_paid})
                                        break

                                    else:
                                        return -1

                            if found == 0:
                                print("Enter correct package id!")

                            return 0
                        output = confirmation(user_package_input)

                        if output == -1:
                            continue
                        else:

                            break

                if found == 0:
                    print('Incorrect Coach choice!')
                    continue
                