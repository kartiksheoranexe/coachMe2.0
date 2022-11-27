from django.shortcuts import render, redirect
from django.contrib.auth import login

import requests
import uuid
from time import sleep

from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import generics, permissions
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse

from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView

from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from coachMe.models import Coach, Package, User, Client, Mapping, Transaction, ClientOnboard, Room, Message
from coachMe.serializers import CoachListSerializer, PackageListSerializer, UserSerializer, RegisterUserSerializer
from coachMe.wrappers import *

# Create your views here.


def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})



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


class RegisterAsCoachAPI(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr_obj = self.request.user
        if usr_obj:
            if usr_obj.user_type == 'U':
                print("Wlecome to register yourself as a coach : " +
                      usr_obj.first_name)
                sleep(1)
                print("Tell us about yourself : ")
                intro = input()
                sleep(1)
                print("Mention years of experience : ")
                exp = float(input())
                sleep(1)
                coach_obj, created = Coach.objects.get_or_create(
                    user=usr_obj, bio=intro, years_of_experience=exp)
                usr_obj.user_type == 'C'
                usr_obj.save()
                return Response({"Coach Registered Successfully!"})
            else:
                return Response({"Already a Coach/Client obj exists for this user."})

        else:
            return Response({"No user exists!"})


class CoachListAPIView(generics.ListAPIView):
    queryset = Coach.objects.all()
    serializer_class = CoachListSerializer


class DisplayPackageAPIView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer


class PurchasePackageAPIView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        print("Welcome to CoachMe Application!")
        sleep(1)
        print("Start your transformation journey today!")
        sleep(1)
        print("Welcome !  " + current_user.first_name)
        if (current_user.user_type == 'U') or (current_user.user_type == 'L'):
            url = 'http://127.0.0.1:8000/coach_me/coach_list/'
            data = {}
            coach_api_call = requests.get(url, headers={}, data=data)

            while True:
                print("Coache's available: ")
                sleep(1)
                coach_list = coach_api_call.json()
                for select_coach in coach_list:
                    print(select_coach['coach_name'])
                print("Select a coach : ")
                sleep(1)
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
                        sleep(1)
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
                                package_obj = Package.objects.filter(
                                    id=i.id).first()
                                if user_package_input == pkg_id:
                                    found = 1
                                    print(user_package_input)
                                    print("Amount to be paid : ",
                                          int(purchase_amount))
                                    print(
                                        "Type Yes to confirm or No to return to the coach list")
                                    sleep(1)
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
                                        sleep(1)
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

                                        print({"Coach Hired!": "Success!", "Coach": coach_obj.user.first_name,
                                              "Client": current_user.first_name, "Package": pckg_name, "Price": amount_paid})
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


class ClientInfoAPIView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        usr_obj = self.request.user
        client_obj = Client.objects.filter(user=usr_obj)[0]
        mapping_obj = Mapping.objects.filter(client_id=client_obj)[0]
        pckg_name = mapping_obj.package_id.package_name
        coach_name = mapping_obj.coach_id.user.first_name
        client_name = mapping_obj.client.user.first_name
        return Response({"package_id ": pckg_name, "coach_id ": coach_name, "price": mapping_obj.price, "client ": client_name})


class OnboardingAPIView(APIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr_obj = self.request.user
        if usr_obj:
            client_obj = Client.objects.filter(user=usr_obj)[0]
            coach_obj = client_obj.coach
            print("Welcome to the Client Onboarding Section!!" +
                  " " + usr_obj.first_name)
            sleep(1)
            print("What is your goal ? ")
            f_goal = input()
            sleep(1)
            print("Please enter your height in feet : ")
            c_height = float(input())
            sleep(1)
            print("Please enter your weight in kg : ")
            c_weight = float(input())
            sleep(1)
            print("Please tell your measurements in inches : ")
            sleep(1)
            print("Neck : ")
            c_neck = float(input())
            print("Shoulder : ")
            c_shoulder = float(input())
            print("Waist : ")
            c_waist = float(input())
            print("Quad : ")
            c_quad = float(input())
            print("Calve : ")
            c_calve = float(input())
            sleep(1)
            print("What is your daily activity level ? ")
            print("Rate out of 10")
            act_lvl = int(input())
            print("Can you join gym? Type Y for yes or N for no")
            gym_availability = input()
            sleep(1)
            print("What is your current workout pattern/split? (Ans in detail)")
            c_wrk_splt = input()
            sleep(1)
            print("What is your preferrable workout timings ? ")
            prf_wrk_tim = input()
            sleep(1)
            print("What is your average sleeping hours ? ")
            avg_sh = int(input())
            sleep(1)
            print("Rate your sleep quality out of 10 : ")
            c_sleep = int(input())
            sleep(1)
            print("Rate your stress levels out of 10 : ")
            c_stress = int(input())
            sleep(1)
            print("Any difficulties you face during doing a specific movement ? ")
            diff_mov = input()
            sleep(1)
            print("Please mention if you have any health related issues : ")
            c_health = input()
            sleep(1)
            print("What current supplements you are using ? ")
            c_supp = input()
            sleep(1)
            print("Have you ever used anabolics ? Type Y for yes or N for no")
            c_ana = input()
            if c_ana == 'Y':
                print("Mention salt names and dosages : ")
                c_ana_des = input()
            else:
                c_ana_des = "NO"
            sleep(1)
            print("Please mention your past/current injuries : ")
            inj = input()
            sleep(1)
            print("Vegeterian or Non-Vegeterian ? ")
            print("Type V for veg or N for non-veg")
            vg = input()
            sleep(1)
            print("How many meals you can take per day? Mention all the possibilities")
            no_meals = input()
            sleep(1)
            print("What is your current eating pattern ? Explain in detail")
            c_eating = input()
            sleep(1)
            print(
                "Tell food choices that you can't ignore ? Will try best to include but NO PROMISES!")
            ch_meal = input()
            sleep(1)
            print("Mention food sources that are easily in reach ?")
            food_srcs = input()
            sleep(1)
            print("What are your expectations from your coach ? ")
            excpttns = input()
            onboard, created = ClientOnboard.objects.get_or_create(coach=coach_obj, client=client_obj,
                                                                   goal=f_goal, height=c_height, weight=c_weight, neck_inches=c_neck, shoulder_inches=c_shoulder,
                                                                   waist_inches=c_waist, quads_inches=c_quad, calf_inches=c_calve, daily_act_level=act_lvl,
                                                                   gym_join=gym_availability, curr_workout_patt=c_wrk_splt, pref_workout_time=prf_wrk_tim,
                                                                   avg_sleeping_hours=avg_sh, sleep_quality=c_sleep, stress_levels=c_stress, any_diff_mov=diff_mov,
                                                                   health_related_issues=c_health, supps=c_supp, anabolics=c_ana, anabolics_desc=c_ana_des,
                                                                   past_curr_injuries=inj, veg_non_veg=vg, no_of_meals=no_meals, curr_eating_pattern=c_eating,
                                                                   cheat_meals=ch_meal, easily_reach_food=food_srcs, expectations_from_caoch=excpttns)
            print("Thank You!")
            print("Welcome to the " + coach_obj.user.first_name + "'s" + " team!!!")
            return Response({"coach ": coach_obj.user.first_name, "client ": client_obj.user.first_name,
                             "goal ": f_goal, "height": c_height, "weight ": c_weight, "neck_inches ": c_neck, "shoulder_inches ": c_shoulder,
                             "waist_inches ": c_waist, "quads_inches ": c_quad, "calf_inches": c_calve, "daily_act_level ": act_lvl,
                             "gym_join ": gym_availability, "curr_workout_patt ":  c_wrk_splt, "pref_workout_time ": prf_wrk_tim,
                             "avg_sleeping_hours": avg_sh, "sleep_quality": c_sleep, "stress_levels": c_stress, "any_diff_mov": diff_mov,
                             "health_related_issues": c_health, "supps": c_supp, "anabolics": c_ana, "anabolics_desc": c_ana_des,
                             "past_curr_injuries": inj, "veg_non_veg": vg, "no_of_meals": no_meals, "curr_eating_pattern": c_eating,
                             "cheat_meals": ch_meal, "easily_reach_food": food_srcs, "expectations_from_caoch": excpttns})
        else:
            return Response({"No User Found!!"})


class SendEmailAPIView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr_obj = self.request.user
        client_obj = Client.objects.filter(user=usr_obj)[0]
        client_email = client_obj.user.email
        coach_email = client_obj.coach.user.email
        # email functionality to send client onboarding excel file to client email's
        port = 587
        # For starttls
        smtp_server = "smtp.gmail.com"
        subject = "Find Client onboarding file in attachment"
        body = "An automated email with Client onboarding file in attachment"
        sender_email = coach_email
        receiver_email = client_email
        # password = input("Type your password : ")
        password = "cvkxfyohyoqxxsno"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email

        message.attach(MIMEText(body, "plain"))

        filename = "D:\CoachMe\coachMe\coachMe\Clientonboard.xlsx"

        with open(filename, "rb") as attachment:
            # Add file as application/vnd.ms-excel
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "vnd.ms-excel")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        return Response({"Email Sent Successfully!!"})


class ParseOnboardAPIView(generics.ListAPIView):
    permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        usr_obj = self.request.user
        if usr_obj:
            if usr_obj.user_type == 'U' or usr_obj.user_type == 'L':
                client_obj = Client.objects.filter(user=usr_obj)[0]
                coach_obj = client_obj.coach
                try:
                    onboard_file = request.FILES['ClientOnboard']
                    if (str(onboard_file).split('.')[-1] == "xls"):
                        data = xls_get(onboard_file, column_limit=2)
                    elif (str(onboard_file).split('.')[-1] == "xlsx"):
                        data = xlsx_get(onboard_file, column_limit=2)
                        # print(data)
                        onboard_data = data["Onboard Tab"]
                        # print(onboard_data)

                        if (len(onboard_data) > 1):
                            new_onb = []
                            for onb_data in onboard_data:
                                for y in onb_data:
                                    new_onb.append(y)
                            # print(new_onb)
                            if (len(new_onb) > 0):

                                if (new_onb[0] == "Goal (Lifestyle/Natural body building)"):

                                    ana = new_onb[48]
                                    check_y = "yes"
                                    if check_y in ana.lower():

                                        output = "Y"

                                        onb_obj, created = ClientOnboard.objects.get_or_create(coach=coach_obj, client=client_obj, goal=new_onb[0], height=new_onb[11], weight=new_onb[13], neck_inches=new_onb[16], chest_inches=new_onb[20], shoulder_inches=new_onb[18], waist_inches=new_onb[22], quads_inches=new_onb[26], calf_inches=new_onb[24], daily_act_level=new_onb[28], gym_join=new_onb[30], curr_workout_patt=new_onb[32], pref_workout_time=new_onb[
                                            34], avg_sleeping_hours=new_onb[36], sleep_quality=new_onb[38], stress_levels=new_onb[40], any_diff_mov=new_onb[42], health_related_issues=new_onb[44], supps=new_onb[46], anabolics=output, anabolics_desc=new_onb[48], past_curr_injuries=new_onb[50], veg_non_veg=new_onb[52], no_of_meals=new_onb[54], curr_eating_pattern=new_onb[56], cheat_meals=new_onb[58], easily_reach_food=new_onb[60], expectations_from_caoch=new_onb[61])
                                        return Response({"Successfully client onboarded object created!"})
                                    else:
                                        output = "N"
                                        onb_obj, created = ClientOnboard.objects.get_or_create(coach=coach_obj, client=client_obj, goal=new_onb[0], height=new_onb[11], weight=new_onb[13], neck_inches=new_onb[16], chest_inches=new_onb[20], shoulder_inches=new_onb[18], waist_inches=new_onb[22], quads_inches=new_onb[26], calf_inches=new_onb[24], daily_act_level=new_onb[28], gym_join=new_onb[30], curr_workout_patt=new_onb[32], pref_workout_time=new_onb[
                                                                                               34], avg_sleeping_hours=new_onb[36], sleep_quality=new_onb[38], stress_levels=new_onb[40], any_diff_mov=new_onb[42], health_related_issues=new_onb[44], supps=new_onb[46], anabolics=output, anabolics_desc=new_onb[48], past_curr_injuries=new_onb[50], veg_non_veg=new_onb[52], no_of_meals=new_onb[54], curr_eating_pattern=new_onb[56], cheat_meals=new_onb[58], easily_reach_food=new_onb[60], expectations_from_caoch=new_onb[61])
                                        return Response({"Successfully client onboarded object created!"})
                    else:
                        return Response({"File Upload fail!"})

                except MultiValueDictKeyError:
                    return Response({"No client onboarding file attached!"})
            else:
                return Response({"User is a coach!"})

        else:
            return Response({"No user found !"})
