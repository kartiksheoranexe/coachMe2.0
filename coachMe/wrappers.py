# from coachMe.models import *
# from rest_framework.response import Response
# from rest_framework import generics, permissions

# import email, smtplib, ssl
# from email import encoders
# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# class SendEmail(generics.ListAPIView):
#     permission_class = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         usr_obj = self.request.user
#         client_obj = Client.objects.filter(user=usr_obj)[0]
#         client_email = client_obj.user.email
#         coach_email = client_obj.coach.user.email
#         #email functionality to send client onboarding excel file to client email's
#         port = 587  
#         # For starttls
#         smtp_server = "smtp.gmail.com"
#         subject = "Find Client onboarding file in attachment"
#         body = "An automated email with Client onboarding file in attachment"
#         sender_email = coach_email
#         receiver_email = client_email
#         # password = input("Type your password : ")
#         password = "cvkxfyohyoqxxsno"

#         message = MIMEMultipart()
#         message["From"] = sender_email
#         message["To"] = receiver_email
#         message["Subject"] = subject
#         message["Bcc"] = receiver_email

#         message.attach(MIMEText(body, "plain"))

#         filename = "D:\CoachMe\coachMe\coachMe\Clientonboard.xlsx"

#         with open(filename, "rb") as attachment:
#             # Add file as application/vnd.ms-excel
#             # Email client can usually download this automatically as attachment
#             part = MIMEBase("application", "vnd.ms-excel")
#             part.set_payload(attachment.read())

#         # Encode file in ASCII characters to send by email    
#         encoders.encode_base64(part)

#         part.add_header(
#             "Content-Disposition",
#             f"attachment; filename= {filename}",
#         )

#         message.attach(part)
#         text = message.as_string()

#         context = ssl.create_default_context()
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.ehlo()  # Can be omitted
#             server.starttls(context=context)
#             server.ehlo()  # Can be omitted
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, text)

#         return Response({"Email Sent Successfully!!"})


