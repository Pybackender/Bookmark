from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
import datetime
import re
from .functions import create_hash_token, create_otp_code, CsrfExemptSessionAuthentication, get_user_info
from .serializers import RoleSerializer
from .authentication import create_refresh_token, get_user_by_token, set_cookie_for_user
from .permissions import AllowAnyUser, IsAuthenticatedUser
from .models import OtpCode, User, Role


# ? First step of login check phone number
class CheckPhoneView(APIView):
    """
            Check phone number if it's not exist create new user
            check if user exist (send otp code)
            check if user exist and has password
            check if user rejected or not
    """
    permission_classes = [AllowAnyUser, ]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        phone = request.data.get('phone')
        is_loggin = False
        has_password = False
        is_admin = False

        if not phone:
            return Response({'detail': 'لطفا شماره تماس را وارد کنید.', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if len(phone) != 11:
            return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        regex = re.compile(r'^09\d{9}$')
        if not regex.match(phone):
            return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if user:
            is_loggin = True
            if user.status == -1:
                return Response({'detail': 'حساب کاربری شما مسدود شده است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

            if user.password:
                if user.role.name == 'admin':
                    is_admin = True
                has_password = True
                return Response({"is_loggin": is_loggin, 'is_admin': is_admin, "has_password": has_password, 'detail': 'پسورد خود را وارد کنید', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

            hash_code = create_hash_token()
            create_otp_code(request, phone, hash_code)
            return Response({'is_loggin': is_loggin, 'is_admin': is_admin, 'has_password': has_password, 'token': hash_code, 'detail': 'کد تایید برای شما ارسال شد', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

        return Response({'is_loggin': is_loggin, 'is_admin': is_admin, 'has_password': has_password, 'detail': 'شماره تلفن وارد شده در سیستم موجود نیست', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


# ? Second step of login check otp code
class AuthenticatedView(APIView):
    """
            register user and send otp code
    """
    permission_classes = [AllowAnyUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        phone = request.data.get('phone')
        is_loggin = False

        user = User.objects.filter(phone=phone).first()
        if user:
            return Response({'detail': 'شماره تلفن وارد شده در سیستم موجود است', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

        if len(phone) != 11:
            return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        role = Role.objects.filter(id=request.data.get('role')).first()
        if not role:
            return Response({'detail': 'نقش را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        # 3= advisor(moshaver), 4= real_estate(daftar), 5= owner(malek/kharidar), 6= free_advisor(moshaverazad)
        roles = [3, 4, 5, 6]
        if role.id not in roles:
            return Response({'detail': 'نقش وارد شده صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        fullname = request.data.get('fullname')

        if not fullname:
            return Response({'detail': 'لطفا نام را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if 2 >= len(fullname) or len(fullname) > 50:
            return Response({'detail': 'نام وارد شده باید بیشتر از 2 کاراکتر باشد', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        # Create hash code for phone number
        hash_code = create_hash_token()
        create_otp_code(request, phone, hash_code)

        return Response({"is_loggin": is_loggin, 'detail': 'کد تایید برای شما ارسال شد', 'token': hash_code, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


# ? Verify code
class VerifyCodeView(APIView):
    """
            Verify code for register
            Verify code for login
            Verify code for reset password
    """
    permission_classes = [AllowAnyUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        phone = request.data.get('phone')
        fullname = request.data.get('fullname')
        role = request.data.get('role')
        token = request.data.get('token')
        code = request.data.get('code')
        # 333
        phone = request.data.get('phone')  # test phone
        token = request.data.get('token')  # test token
        code = request.data.get('code')  # test code

        role = Role.objects.filter(id=role).first()

        print(f"Phone: {phone}, Token: {token}, Code: {code}")  # test
        if not phone:
            return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({'detail': 'لطفا کد تایید را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        check_code = OtpCode.objects.filter(
            phone=phone, token=token, code=code).first()
        if not check_code:
            return Response({'detail': 'کد تایید نامعتبر است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not check_code.code:
            return Response({'detail': 'کد تاییدی برای شما ارسال نشده است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if user:
            if check_code.code == code:
                check_code.delete()
                update_last_login(None, user)
                refresh_token = create_refresh_token(
                    user.id, user.fullname, user.role.id, user.phone)
                response = set_cookie_for_user(request, refresh_token)
                response.data = {
                    'detail': 'یوزر با موفقیت وارد شد',
                    'status': status.HTTP_200_OK,
                }
                return response
            else:
                return Response({'detail': 'کد تایید صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not fullname:
            return Response({'detail': 'لطفا نام را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not role:
            return Response({'detail': 'لطفا نقش را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        expire_date = check_code.request_date
        expire_date = expire_date + datetime.timedelta(minutes=2)

        if expire_date < timezone.now():
            check_code.delete()
            return Response({'detail': 'کد تایید منقضی شده است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if check_code.code == code:
            user = User.objects.create(
                phone=phone,
                fullname=fullname,
                role=role,
            )
            check_code.delete()

            refresh_token = create_refresh_token(
                user.id, fullname, role.id, phone)
            response = set_cookie_for_user(request, refresh_token)
            response.data = {
                'message': 'ثبت نام با موفقیت انجام شد',
                'status': status.HTTP_200_OK,
            }
            return response

        return Response({'detail': 'کد تایید نامعتبر است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class CheckPasswordView(APIView):
    """
    Check password if user saved password
    """
    permission_classes = [AllowAnyUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not phone:
            return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({'detail': 'لطفا رمز عبور را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({'detail': 'کاربری با این شماره وجود ندارد', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'detail': 'رمز عبور اشتباه است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        # Update last login and create refresh token
        update_last_login(None, user)
        if user.role.id == 1:
            refresh_token = create_refresh_token(
                user.id, user.fullname, user.role.id, user.phone)
        else:
            refresh_token = create_refresh_token(
                user.id, user.fullname, user.role.id, user.phone)

        # No need to decode refresh_token if it's already a string
        response = set_cookie_for_user(request, refresh_token)
        response.data = {
            'detail': 'یوزر با موفقیت وارد شد',
            'status': status.HTTP_200_OK,
        }
        return response

# ? Forgot Password


class ForgotPasswordView(APIView):
    """
            forgot password if user forget password
    """
    permission_classes = [AllowAnyUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()
        if not user:
            return Response({'detail': 'کاربری با این شماره وجود ندارد', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            hash_code = create_hash_token()
            create_otp_code(request, phone, hash_code)
            return Response({'detail': 'کد تایید برای شما ارسال شد', 'token': hash_code, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


# ? logout user
class LogoutView(APIView):
    """
            logout user and delete cookie
    """
    permission_classes = [IsAuthenticatedUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request):
        response = Response()
        # current_site = Site.objects.get_current()
        # current_site = f".{current_site.domain}"
        # !TODO domain=current_site (this is for production)
        response.delete_cookie('Authorization')
        response.data = {
            'message': 'خروج با موفقیت انجام شد',
            'status': status.HTTP_200_OK,
        }
        return response

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


# ? check user
class UserView(APIView):
    """
            check user if user login
            check user info
    """
    permission_classes = [IsAuthenticatedUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        user = get_user_by_token(request)
        if user:
            return Response({
                'data': get_user_info(user)
            })

        else:
            return Response({'detail': 'کاربری یافت نشد', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

    def permission_denied(self, request, message=None, code=None):
        raise PermissionDenied(message)


# ? check role for user
class RoleView(APIView):
    """
            show all roles for user
    """
    permission_classes = [AllowAnyUser]
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)