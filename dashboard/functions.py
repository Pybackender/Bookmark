
# # from rest_framework.validators import ValidationError
# # from django.utils.crypto import get_random_string
# # from rest_framework.response import Response
# # from rest_framework import status
# # import random
# # from rest_framework.authentication import SessionAuthentication

# # from dashboard.models import OtpCode


# # from .utils import send_otp_code


# # # ? Create hash token
# # def create_hash_token():
# #     """
# #             Generate a random string of 25 characters
# #             This will be used as the hash token for the OTP code
# #     """
# #     hash_str = "000005fab4534d05api_key9a0554259914a86fb9e7eb014e4e5d52permswrite"
# #     hash_str = ("".join(random.sample(hash_str, 25)))
# #     return hash_str


# # def create_otp_code(request, phone, token):
# #     """
# #             Create a code for sms verification
# #     """
# #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# #     if x_forwarded_for:
# #         ip_address = x_forwarded_for.split(',')[-1].strip()
# #         return Response({'detail': "وی پی ان خود را قطع کنید سپس وارد شوید", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
# #     else:
# #         ip_address = request.META.get('REMOTE_ADDR')

# #     # check_ip = OtpCode.objects.filter(ip_address=ip_address)
# #     random_code = get_random_string(length=4, allowed_chars='1234567890')

# #     check_ip = OtpCode.objects.filter(ip_address=ip_address)
# #     for qs in check_ip:
# #         if ip_address == qs.ip_address:
# #             if check_ip.count() > 2:
# #                 raise ValidationError(
# #                     {'detail': "تعداد درخواست های شما بیشتر از حد مجاز است بعد از 5 دقیقه دوباره تلاش کنید"})

# #         if phone == qs.phone:
# #             get_code = qs.code
# #             otp_code = OtpCode.objects.create(
# #                 phone=phone, token=token, code=get_code, ip_address=ip_address)
# #             return otp_code

# #     otp_code = OtpCode.objects.create(
# #         phone=phone, token=token, code=random_code, ip_address=ip_address)
# #     send_otp_code(phone, random_code)
# #     return otp_code

# # class CsrfExemptSessionAuthentication(SessionAuthentication):
# #     def enforce_csrf(self, request):
# #         return


# from rest_framework.validators import ValidationError
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.authentication import SessionAuthentication
# from kavenegar import KavenegarAPI
# from dashboard.models import OtpCode
# import random

# # ? Create hash token
# def create_hash_token():
#     hash_str = "000005fab4534d05api_key9a0554259914a86fb9e7eb014e4e5d52permswrite"
#     return "".join(random.sample(hash_str, 25))

# def create_otp_code(request, phone, token):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip_address = x_forwarded_for.split(',')[-1].strip()
#         return Response({'detail': "وی پی ان خود را قطع کنید سپس وارد شوید", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         ip_address = request.META.get('REMOTE_ADDR')

#     check_ip = OtpCode.objects.filter(ip_address=ip_address)
#     for qs in check_ip:
#         if ip_address == qs.ip_address:
#             if check_ip.count() > 2:
#                 raise ValidationError(
#                     {'detail': "تعداد درخواست های شما بیشتر از حد مجاز است بعد از 5 دقیقه دوباره تلاش کنید"})

#         if phone == qs.phone:
#             get_code = qs.code
#             otp_code = OtpCode.objects.create(
#                 phone=phone, token=token, code=get_code, ip_address=ip_address)
#             return otp_code

#     # Generate a new OTP code using the dedicated function
#     random_code = generate_random_otp(length=4)

#     otp_code = OtpCode.objects.create(
#         phone=phone, token=token, code=random_code, ip_address=ip_address)

#     # Send the OTP code via SMS
#     send_otp_code(phone, random_code)
#     return otp_code

# def generate_random_otp(length=4):
#     """تولید یک کد OTP تصادفی با طول مشخص"""
#     return ''.join(random.choices('0123456789', k=length))

# def send_otp_code(phone, otp):
#     print(f"Generated OTP: {otp}")  # Print OTP to console
#     api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')  # Replace with your API key

#     # Parameters for sending SMS
#     params = {
#         'sender': '2000660110',  # Sender number
#         'receptor': phone,        # Recipient number
#         'message': f'کد تایید شما: {otp}'  # Message including OTP
#     }

#     try:
#         response = api.sms_send(params)  # Send SMS
#         print(f"OTP {otp} sent to {phone}. Response: {response}")
#     except Exception as e:
#         print(f"Failed to send OTP. Error: {str(e)}")

# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         return


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
##############################################

# def create_otp_code(request, phone, token):
#     """
#     Create a code for SMS verification
#     """
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip_address = x_forwarded_for.split(',')[-1].strip()
#         return Response({'detail': "وی پی ان خود را قطع کنید سپس وارد شوید", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         ip_address = request.META.get('REMOTE_ADDR')

#     # Generate a random OTP code
#     random_code = get_random_string(length=4, allowed_chars='1234567890')

#     # Print the OTP code to the terminal
#     # این خط کد OTP را در ترمینال چاپ می‌کند
#     print(f"Generated OTP Code for {phone}: {random_code}")

#     check_ip = OtpCode.objects.filter(ip_address=ip_address)
#     for qs in check_ip:
#         if ip_address == qs.ip_address:
#             if check_ip.count() > 20:
#                 raise ValidationError(
#                     {'detail': "تعداد درخواست های شما بیشتر از حد مجاز است بعد از 5 دقیقه دوباره تلاش کنید"})

#         if phone == qs.phone:
#             get_code = qs.code
#             otp_code = OtpCode.objects.create(
#                 phone=phone, token=token, code=get_code, ip_address=ip_address)
#             return otp_code

#     otp_code = OtpCode.objects.create(
#         phone=phone, token=token, code=random_code, ip_address=ip_address)

#     delete_useless_otp_code()
#     # Send the OTP code to the phone
#     send_otp_code(phone, random_code)

#     return otp_code

# ? get user info


def get_user_info(user):
    role = {
        'id': user.role.id,
        'name': user.role.name,
        "display_name": user.role.display_name,
    }
    if user.role.id == 1:
        city = None
    else:
        city = {
            'id': user.city.id,
            'name': user.city.name,
        }

    roles = [1, 2, 5, 6]
    if user.role.id in roles:
        company_name = ""
    else:
        company_name = {
            'id': user.company_name.id,
            'name': user.company_name.name,
            'username': user.company_name.owner.fullname,
            'phone': user.company_name.owner.phone,
        }

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

    order_count = Order.objects.filter(user=user).count()

    data = {
        'id': user.id,
        'fullname': user.fullname,
        'phone': user.phone,
        'role': role,
        'city': city,
        'company_name': company_name,
        'avatar': avatar,
        'user_meta': data,
        'has_password': has_password,
        'status': status,
        'order_count': order_count,
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
