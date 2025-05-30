from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.validators import ValidationError
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework import status
import random

from dashboard.cron import delete_useless_otp_code
from dashboard.models import OtpCode

from .utils import send_otp_code


# ? Create hash token
def create_hash_token():
    """
            Generate a random string of 25 characters
            This will be used as the hash token for the OTP code 
    """
    hash_str = "000005fab4534d05api_key9a0554259914a86fb9e7eb014e4e5d52permswrite"
    hash_str = ("".join(random.sample(hash_str, 25)))
    return hash_str

def create_otp_code(request, phone, token):
    """
    Create a code for SMS verification.
    """
    # Get the client's IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip_address = x_forwarded_for.split(',')[-1].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')

    # Block VPN users
    if x_forwarded_for:
        return Response({'detail': "وی پی ان خود را قطع کنید سپس وارد شوید", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a random OTP code
    random_code = get_random_string(length=4, allowed_chars='1234567890')
    print(f"Generated OTP Code for {phone}: {random_code}")  # Debugging line

    # Check the number of requests from the same IP
    if OtpCode.objects.filter(ip_address=ip_address).count() > 20:
        raise ValidationError({'detail': "تعداد درخواست های شما بیشتر از حد مجاز است بعد از 5 دقیقه دوباره تلاش کنید"})

    # Check if there's an existing OTP for the same phone number
    existing_otp = OtpCode.objects.filter(phone=phone).first()
    if existing_otp:
        # Use the existing OTP code if it exists
        otp_code = existing_otp
    else:
        # Create a new OTP code
        otp_code = OtpCode.objects.create(
            phone=phone,
            token=token,
            code=random_code,
            ip_address=ip_address
        )

    # Clean up old OTP codes
    delete_useless_otp_code()

    # Send the OTP code to the phone
    send_otp_code(phone, otp_code.code)

    return Response({'detail': "کد تایید ارسال شد", 'otp_code': otp_code.code}, status=status.HTTP_201_CREATED)
# ? get user info


def get_user_info(user):
    role = {
        'id': user.role.id,
        'name': user.role.name,
        "display_name": user.role.display_name,
    }
    if user.role.id == 1:
        roles = [1, 2, 5, 6]
    if user.role.id in roles:
        pass
    # get avatar
    avatar = user.avatar

    # get status id and name
    status = {
        'id': user.status,
        'name': user.get_status_display(),
    }

    # check has password
    if user.password:
        has_password = True
    else:
        has_password = False

    data = {
        'id': user.id,
        'fullname': user.fullname,
        'phone': user.phone,
        'role': role,
        'avatar': avatar,
        'user_meta': data,
        'has_password': has_password,
        'status': status,
    }
    return data


# ? Check user is active
def check_user_is_active(user):
    if user.status != 1:
        raise PermissionDenied('حساب کاربری شما فعال نیست')


#! Handle the csrf error for production
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
