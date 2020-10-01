from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import MyUser
from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException



#SMS Verification using Twilio (https://www.twilio.com/docs/verify/api)
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
service_id = settings.TWILIO_SERVICE_ID


client = Client(account_sid, auth_token)


def send_otp(email_id, phone_num):
    """
    Sends OTP to both SMS and Email Address.
    """
    phone_verification = client.verify \
                .services(service_id) \
                .verifications \
                .create(to=phone_num, channel='sms')

    # email_verification = client.verify \
    #             .services(service_id) \
    #             .verifications \
    #             .create(to=email_id, channel='email')



def verify_otp(email_id, phone_num, email_code, phone_code):
    """
    Verify OTP after it has been sent. Both email and phone number get different codes.
    """
    try:
        phone_verification_check = client.verify \
                        .services(service_id) \
                        .verification_checks \
                        .create(to=phone_num, code=phone_code)

        email_verification_check = client.verify \
                        .services(service_id) \
                        .verification_checks \
                        .create(to=email_id, code=email_code)

    except TwilioRestException:
        return False

    if phone_verification_check.status == email_verification_check.status == 'approved':
        return True

class PasswordlessAuthBackend(ModelBackend):
    def start_auth(self, username=None):
        try:
            user =  MyUser.objects.get(username=username) #get the user object from email id
            send_otp(email_id=user.email, phone_num=user.phone_num) #send otp to both email and phone
            return user
        except:
            return None

    def get_user(self, username):
        try:
            return MyUser.objects.get(username=username)
        except:
            return None
