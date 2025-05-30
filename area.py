# ############## user_area
# # model

# class OtpCode(models.Model):
#     """
#             create code for sms verification
#     """
#     phone = models.CharField(max_length=11)
#     ip_address = models.CharField(max_length=255)
#     code = models.PositiveIntegerField()
#     token = models.CharField(max_length=255, null=True, blank=True)
#     request_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.phone
    
# # functions.py

# def create_otp_code(request, phone, token):
# 	"""
# 		Create a code for sms verification
# 	"""
# 	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
# 	if x_forwarded_for:
# 		ip_address = x_forwarded_for.split(',')[-1].strip()
# 		return Response({'detail': "وی پی ان خود را قطع کنید سپس وارد شوید", 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
# 	else:
# 		ip_address = request.META.get('REMOTE_ADDR')
	
# 	# check_ip = OtpCode.objects.filter(ip_address=ip_address)
# 	random_code = get_random_string(length=4, allowed_chars='1234567890')
	
# 	check_ip = OtpCode.objects.filter(ip_address=ip_address)
# 	for qs in check_ip:
# 		if ip_address == qs.ip_address:
# 			if check_ip.count() > 2:
# 				raise ValidationError({'detail': "تعداد درخواست های شما بیشتر از حد مجاز است بعد از 5 دقیقه دوباره تلاش کنید"})

# 		if phone == qs.phone:
# 			get_code = qs.code
# 			otp_code = OtpCode.objects.create(phone=phone, token=token, code=get_code, ip_address=ip_address)
# 			return otp_code
				
# 	otp_code = OtpCode.objects.create(phone=phone, token=token, code=random_code, ip_address=ip_address)
# 	send_otp_code(phone, random_code)
# 	return otp_code
# # utils.py

# from kavenegar import *



# def send_otp_code(phone, code):
# 	#? send sms to user
# 	# try:
# 	# 	api = KavenegarAPI('6362784C70776C357562616664687A364F3256574F4E69624D356965774163697672346A7461552F755A453D')
		
# 	# 	params = {
# 	# 		'sender': '', #optional
# 	# 		'template': 'otp',
# 	# 		'receptor': phone, #multiple mobile number, split by comma
# 	# 		'token': code,
# 	# 		'type': 'sms'
# 	# 	}
# 	# 	response = api.verify_lookup(params)
# 	# 	print(response)
# 	# except APIException as e:
# 	# 	print(e)
# 	# except HTTPException as e:
# 	# 	print(e)
# 	pass

# #TODO about payment sms
# def send_notif_sms(phone, adcode):
# 	try:
# 		api = KavenegarAPI('6362784C70776C357562616664687A364F3256574F4E69624D356965774163697672346A7461552F755A453D')
		
# 		params = {
# 			'sender': '', #optional
# 			'template': 'notif',
# 			'receptor': phone, #multiple mobile number, split by comma
# 			'type': 'sms',
# 			'token': adcode,
# 		}
# 		response = api.verify_lookup(params)
# 	except APIException as e:
# 		print(e)
# 	except HTTPException as e:
# 		print(e)

# # cron.py

# from django.utils.timezone import now, timedelta

# from .models import OtpCode, VipSms
# from .utils import send_notif_sms
# from post_manager.models import PackageOption

# # Delete Useless OtpCode
# def delete_useless_otp_code():

# 	"""
# 		Delete useless code in otp_code table
# 		This function will be called every 5 minutes
# 		Call this function in the settings.py file
# 	"""
# 	print('ok')
# 	expired_date = now() - timedelta(minutes=5)
# 	OtpCode.objects.filter(request_date__lt=expired_date).delete()
	
# # admin 

# class OtpCodeAdmin(admin.ModelAdmin):
# 	list_display = ('phone', 'code', 'ip_address')
# 	list_filter =  ('phone',)
# 	readonly_fields = ('request_date',)
# admin.site.register(OtpCode, OtpCodeAdmin)

# # views.py 

# from rest_framework.authentication import BasicAuthentication 
# from rest_framework.exceptions import AuthenticationFailed
# from rest_framework.decorators import permission_classes
# from django.contrib.auth.models import update_last_login
# from rest_framework.exceptions import PermissionDenied
# from django.views.decorators.csrf import csrf_protect
# from rest_framework import generics, viewsets, status
# from django.utils.timezone import utc, now, timedelta
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.sites.models import Site
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.http import JsonResponse
# from django.db.models import F

# import datetime, re

# from .functions import create_hash_token, create_otp_code, CsrfExemptSessionAuthentication, get_user_info, check_user_is_active
# from .serializers import CompanySerializer, RoleSerializer, CitySerializer, OrderSerializer, PackageSerializer
# from .authentication import create_refresh_token, get_user_by_token, set_cookie_for_user
# from .permissions import AllowAnyUser, IsAuthenticatedUser
# from .models import User, Company, Role, City, OtpCode, Province
# from .paginations import PageNumberAsLimitOffset
# from .zarinpal import *
# from .payment import *

# from post_manager.models import Category, Ad, Order, Package, Payment, PackageOption, VipSms
# from post_manager.serializers import AdSerializer, AdPreviewSerializer


# #? First step of login check phone number
# class CheckPhoneView(APIView):
# 	"""
# 		Check phone number if it's not exist create new user
# 		check if user exist (send otp code)
# 		check if user exist and has password
# 		check if user rejected or not
# 	"""
# 	permission_classes = [AllowAnyUser, ]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def post(self, request):
# 		phone = request.data.get('phone')
# 		is_loggin = False
# 		has_password = False
# 		is_admin = False
	
# 		if not phone:
# 			return Response({'detail': 'لطفا شماره تماس را وارد کنید.', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		if len(phone) != 11:
# 			return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		regex = re.compile(r'^09\d{9}$')
# 		if not regex.match(phone):
# 			return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		user= User.objects.filter(phone=phone).first()
# 		if user:
# 			is_loggin = True
# 			if user.status == -1:
# 				return Response({'detail': 'حساب کاربری شما مسدود شده است', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 			if user.password:
# 				if user.role.name == 'admin':
# 					is_admin = True
# 				has_password = True
# 				return Response({"is_loggin": is_loggin, 'is_admin': is_admin, "has_password":has_password, 'detail': 'پسورد خود را وارد کنید', 'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
			
# 			hash_code = create_hash_token()
# 			create_otp_code(request, phone, hash_code)
# 			return Response({'is_loggin':is_loggin, 'is_admin': is_admin, 'has_password':has_password , 'token': hash_code, 'detail': 'کد تایید برای شما ارسال شد', 'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
		
# 		return Response({'is_loggin':is_loggin, 'is_admin': is_admin, 'has_password':has_password, 'detail': 'شماره تلفن وارد شده در سیستم موجود نیست', 'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)


# #? Second step of login check otp code
# class AuthenticatedView(APIView):
# 	"""
# 		register user and send otp code
# 	"""
# 	permission_classes = [AllowAnyUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def post(self, request):
# 		phone = request.data.get('phone')
# 		is_loggin = False

# 		user= User.objects.filter(phone=phone).first()
# 		if user:
# 			return Response({'detail': 'شماره تلفن وارد شده در سیستم موجود است', 'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)

# 		if len(phone) != 11:
# 			return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		role = Role.objects.filter(id=request.data.get('role')).first()
# 		if not role:
# 			return Response({'detail': 'نقش را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		roles = [3, 4, 5, 6] # 3= advisor(moshaver), 4= real_estate(daftar), 5= owner(malek/kharidar), 6= free_advisor(moshaverazad)
# 		if role.id not in roles:
# 			return Response({'detail': 'نقش وارد شده صحیح نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		fullname = request.data.get('fullname')
# 		city = request.data.get('city')
		
# 		if not fullname:
# 			return Response({'detail': 'لطفا نام را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		if  2 >= len(fullname) or len(fullname) > 50:
# 			return Response({'detail': 'نام وارد شده باید بیشتر از 2 کاراکتر باشد', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if not city:
# 			return Response({'detail': 'لطفا شهر را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		city = City.objects.filter(id=city).first()
# 		if not city:
# 			return Response({'detail': 'شهر وارد شده معتبر نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		get_company = request.data.get('company_name')
# 		if role.id == 3 or role.id == 4: # Real_estate(daftarAmlak) / advisor(moshaverAmlak)
# 			if not get_company:
# 				return Response({'detail': 'لطفا نام شرکت را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if role.id == 3: # advisor
# 			company_instance = Company.objects.filter(id=get_company).first()
# 			if not company_instance:
# 				return Response({'detail': 'شرکت وارد شده معتبر نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
				
# 			if company_instance.status == 0:
# 				return Response({'detail': 'شرکت وارد شده فعال نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if role.id == 6 or role.id ==5: # Free_advisor, owner
# 			company_instance = None

# 		# Create hash code for phone number
# 		hash_code = create_hash_token()
# 		create_otp_code(request, phone, hash_code)
		
# 		return Response({"is_loggin": is_loggin, 'detail': 'کد تایید برای شما ارسال شد', 'token': hash_code,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)


# #? Verify code 
# class VerifyCodeView(APIView):
# 	"""
# 		Verify code for register
# 		Verify code for login
# 		Verify code for reset password
# 	"""
# 	permission_classes = [AllowAnyUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
	
# 	def post(self, request):
# 		phone = request.data.get('phone')
# 		fullname = request.data.get('fullname')
# 		role = request.data.get('role')
# 		city = request.data.get('city')
# 		company = request.data.get('company_name')
# 		token = request.data.get('token')
# 		code = request.data.get('code')

# 		role =Role.objects.filter(id=role).first()
# 		city = City.objects.filter(id=city).first()

# 		if not phone:
# 			return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if not code:
# 			return Response({'detail': 'لطفا کد تایید را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		check_code = OtpCode.objects.filter(phone=phone, token=token, code=code).first()
# 		if not check_code:
# 			return Response({'detail': 'کد تایید نامعتبر است', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		if not check_code.code:
# 			return Response({'detail': 'کد تاییدی برای شما ارسال نشده است', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		user = User.objects.filter(phone=phone).first()
# 		if user:
# 			if check_code.code == code:
# 				check_code.delete()
# 				update_last_login(None, user)
# 				refresh_token = create_refresh_token(user.id, user.fullname, user.role.id, user.phone, user.city.name)
# 				response = set_cookie_for_user(request, refresh_token)
# 				response.data = {
# 					'detail': 'یوزر با موفقیت وارد شد',
# 					'status':status.HTTP_200_OK,
# 				}
# 				return response
# 			else:
# 				return Response({'detail': 'کد تایید صحیح نیست', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
	
# 		if not fullname:
# 			return Response({'detail': 'لطفا نام را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if not role:
# 			return Response({'detail': 'لطفا نقش را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		if not city:
# 			return Response({'detail': 'لطفا شهر را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# 		expire_date = check_code.request_date
# 		expire_date = expire_date + timedelta(minutes=2)

# 		if expire_date < datetime.datetime.utcnow().replace(tzinfo=utc):
# 			check_code.delete()
# 			return Response({'detail': 'کد تایید منقضی شده است', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if check_code.code == code:
# 			user = User.objects.create(
# 				phone=phone, 
# 				fullname=fullname, 
# 				role=role, 
# 				city=city
# 				)
# 			check_code.delete()

# 			if role.id == 4: # Real_estate/ daftarAmlak
# 				company = Company.objects.create(
# 					name=company,
# 					owner=user
# 				)
# 				user.company_name = company
# 				user.status = 0
# 				user.save()
			
# 			if role.id == 3: # Advisor
# 				company_instance = Company.objects.filter(id=company).first()
# 				user.company_name = company_instance
# 				user.status = 0
# 				user.save()
			
# 			refresh_token = create_refresh_token(user.id, fullname, role.id, phone, city.name)
# 			response = set_cookie_for_user(request, refresh_token)
# 			response.data = {
# 				'message': 'ثبت نام با موفقیت انجام شد',
# 				'status':status.HTTP_200_OK,
# 			}
# 			return response

# 		return Response({'detail': 'کد تایید نامعتبر است', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# #? Check Password 
# class CheckPasswordView(APIView):
# 	"""
# 		check password if user save password
# 	"""
# 	permission_classes = [AllowAnyUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def post(self, request):
# 		phone = request.data.get('phone')
# 		password = request.data.get('password')

# 		if not phone:
# 			return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
			
# 		if not password:
# 			return Response({'detail': 'لطفا رمز عبور را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		user = User.objects.filter(phone=phone).first()
# 		if not user:
# 			return Response({'detail': 'کاربری با این شماره وجود ندارد', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		if not user.check_password(password):
# 			return Response({'detail': 'رمز عبور اشتباه است', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# 		if user.check_password(password):
# 			update_last_login(None, user)
# 			if user.role.id == 1:
# 				refresh_token = create_refresh_token(user.id, user.fullname, user.role.id, user.phone, user.city)
# 			else:
# 				refresh_token = create_refresh_token(user.id, user.fullname, user.role.id, user.phone, user.city.name)
# 			refresh_token = refresh_token.decode('utf-8')
# 			response = set_cookie_for_user(request, refresh_token)
# 			response.data = {
# 				'detail': 'یوزر با موفقیت وارد شد',
# 				'status':status.HTTP_200_OK,
# 			}
# 			return response

# #? Forgot Password
# class ForgotPasswordView(APIView):
# 	"""
# 		forgot password if user forget password
# 	"""
# 	permission_classes = [AllowAnyUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def post(self, request):
# 		phone = request.data.get('phone')
# 		if not phone:
# 			return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		user = User.objects.filter(phone=phone).first()
# 		if not user:
# 			return Response({'detail': 'کاربری با این شماره وجود ندارد', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 		if user:
# 			hash_code = create_hash_token()
# 			create_otp_code(request, phone, hash_code)
# 			return Response({'detail': 'کد تایید برای شما ارسال شد', 'token': hash_code,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)


# #? logout user
# class LogoutView(APIView):
# 	"""
# 		logout user and delete cookie
# 	"""
# 	permission_classes = [IsAuthenticatedUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def post(self, request):
# 		response = Response()
# 		# current_site = Site.objects.get_current()
# 		# current_site = f".{current_site.domain}"
# 		response.delete_cookie('Authorization') #!TODO domain=current_site (this is for production)
# 		response.data = {
# 			'message': 'خروج با موفقیت انجام شد',
# 			'status':status.HTTP_200_OK,
# 		}
# 		return response

# 	def permission_denied(self, request, message=None, code=None):
# 		raise PermissionDenied(message)


# #? check user
# class UserView(APIView):
# 	"""
# 		check user if user login
# 		check user info
# 	"""
# 	permission_classes = [IsAuthenticatedUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def get(self, request):
# 		user = get_user_by_token(request)
# 		if user:
# 			return Response({
# 				'data':get_user_info(user)
# 			})
			
# 		else:
# 			return Response({'detail': 'کاربری یافت نشد', 'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
		
# 	def permission_denied(self, request, message=None, code=None):
# 		raise PermissionDenied(message)


# #? check role for user
# class RoleView(APIView):
# 	"""
# 		show all roles for user
# 	"""
# 	permission_classes = [AllowAnyUser]
# 	authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

# 	def get(self, request):
# 		roles = Role.objects.all()
# 		serializer = RoleSerializer(roles, many=True)
# 		return Response(serializer.data)
	

# ############################################3333
# # meeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee


# # model ####
# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class User(models.Model):
#     username = models.CharField(max_length=150)
#     email = models.EmailField()
#     # Ensure phone is unique
#     phone = models.CharField(max_length=11, unique=True)

#     def __str__(self):
#         return self.username


# class OtpCode(models.Model):
#     """
#             create code for sms verification
#     """
#     phone = models.CharField(max_length=11)
#     ip_address = models.CharField(max_length=255)
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     token = models.CharField(max_length=255, null=True, blank=True)
#     request_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.phone
# # views 

# from rest_framework.authentication import BasicAuthentication 
# from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.contrib.auth.models import update_last_login
# from django.utils import timezone
# from datetime import timedelta
# import re

# from dashbord.models import OtpCode, User

# from .functions import create_hash_token, create_otp_code, CsrfExemptSessionAuthentication
# from .authentication import create_refresh_token, get_user_by_token, set_cookie_for_user
# from .permissions import AllowAnyUser, IsAuthenticatedUser

# # First step of login check phone number
# class CheckPhoneView(APIView):
#     permission_classes = [AllowAnyUser]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     def post(self, request):
#         phone = request.data.get('phone')

#         if not phone:
#             return Response({'detail': 'لطفا شماره تماس را وارد کنید.', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         if len(phone) != 11 or not re.match(r'^09\d{9}$', phone):
#             return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.filter(phone=phone).first()
#         hash_code = create_hash_token()
#         create_otp_code(request, phone, hash_code)

#         if user:
#             return Response({'is_loggin': True, 'has_password': True, 'detail': 'کد تایید برای شما ارسال شد', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

#         return Response({'is_loggin': False, 'has_password': False, 'detail': 'کد تایید برای شما ارسال شد', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

# # Second step of login check otp code
# class AuthenticatedView(APIView):
#     permission_classes = [AllowAnyUser]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     def post(self, request):
#         phone = request.data.get('phone')
#         if not phone or len(phone) != 11 or not re.match(r'^09\d{9}$', phone):
#             return Response({'detail': 'شماره تلفن وارد شده صحیح نیست', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.filter(phone=phone).first()
#         if user:
#             return Response({'detail': 'شماره تلفن وارد شده در سیستم موجود است', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

#         hash_code = create_hash_token()
#         create_otp_code(request, phone, hash_code)
        
#         return Response({"is_loggin": False, 'detail': 'کد تایید برای شما ارسال شد', 'token': hash_code, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

# # Verify code 
# class VerifyCodeView(APIView):
#     permission_classes = [AllowAnyUser]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     def post(self, request):
#         phone = request.data.get('phone')
#         token = request.data.get('token')
#         code = request.data.get('code')

#         if not phone or not code:
#             return Response({'detail': 'لطفا شماره تلفن و کد تایید را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         check_code = OtpCode.objects.filter(phone=phone, token=token, code=code).first()
#         if not check_code:
#             return Response({'detail': 'کد تایید نامعتبر است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         if check_code.request_date + timedelta(minutes=2) < timezone.now():
#             check_code.delete()
#             return Response({'detail': 'کد تایید منقضی شده است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         user, created = User.objects.get_or_create(phone=phone)

#         if created:
#             user.username = f"user_{phone}"  # Generate a default username
#             user.save()

#         check_code.delete()  # Delete OTP after successful verification

#         refresh_token = create_refresh_token(user.id, user.username, user.phone)
#         response = set_cookie_for_user(request, refresh_token)
#         response.data = {
#             'detail': 'ورود با موفقیت انجام شد',
#             'status': status.HTTP_200_OK,
#         }
#         return response

# # Check Password 
# class CheckPasswordView(APIView):
#     permission_classes = [AllowAnyUser]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     def post(self, request):
#         phone = request.data.get('phone')
#         password = request.data.get('password')

#         if not phone or not password:
#             return Response({'detail': 'لطفا شماره تلفن و رمز عبور را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.filter(phone=phone).first()
#         if not user or not user.check_password(password):
#             return Response({'detail': 'کاربری با این شماره وجود ندارد یا رمز عبور اشتباه است', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         update_last_login(None, user)
#         refresh_token = create_refresh_token(user.id, user.fullname, user.role.id, user.phone, user.city.name)
#         response = set_cookie_for_user(request, refresh_token)
#         response.data = {
#             'detail': 'یوزر با موفقیت وارد شد',
#             'status': status.HTTP_200_OK,
#         }
#         return response

# # Forgot Password
# class ForgotPasswordView(APIView):
#     permission_classes = [AllowAnyUser]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     def post(self, request):
#         phone = request.data.get('phone')
#         if not phone:
#             return Response({'detail': 'لطفا شماره تلفن را وارد کنید', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         user = User.objects.filter(phone=phone).first()
#         if not user:
#             return Response({'detail': 'کاربری با این شماره وجود ندارد', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

#         hash_code = create_hash_token()
#         create_otp_code(request, phone, hash_code)
#         return Response({'detail': 'کد تایید برای شما ارسال شد', 'token': hash_code, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

# # Logout user
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticatedUser]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

#     def post(self, request):
#         response = Response()
#         response.delete_cookie('Authorization')  # Handle domain for production if needed
#         response.data = {
#             'message': 'خروج با موفقیت انجام شد',
#             'status': status.HTTP_200_OK,
#         }
#         return response
# # forms 
# from django import forms
# from django.core.exceptions import ValidationError
# from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext as _


# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = get_user_model()
#         fields = UserChangeForm.Meta.fields

# class ChangeUserInfoAfterRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('email', 'password')

#     def clean_password(self):
#         data = self.cleaned_data.get("password")
#         if data and len(data) < 8:
#             raise ValidationError(_("Password must be at least 8 characters"))
#         if data and data.isalpha():
#             raise ValidationError(_("Password must have at least one digit"))
#         if data and data.isdigit():
#             raise ValidationError(_("Password cannot be only a number"))
#         return data

# class ChangeUsersUsernameForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['username']

# class ChangeUsersEmailAddressForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['email']

# class ChangeUsersOTPNumberForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ['phone_number']

# # utils 

# from kavenegar import *
# # from kavenegar import *
# # api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')
# # params = { 'sender' : '2000660110', 'receptor': '09012994672', 'message' :'.وب سرویس پیام کوتاه کاوه نگار' }
# # response = api.sms_send(params)


# def send_otp_code(phone, code):
# 	#? send sms to user
# 	# try:
#     # api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')
		
# 	# 	params = {
# 	# 		'sender': '', #optional
# 	# 		'template': 'otp',
# 	# 		'receptor': phone, #multiple mobile number, split by comma
# 	# 		'token': code,
# 	# 		'type': 'sms'
# 	# 	}
# 	# 	response = api.verify_lookup(params)
# 	# 	print(response)
# 	# except APIException as e:
# 	# 	print(e)
# 	# except HTTPException as e:
# 	# 	print(e)
# 	pass

# #TODO about payment sms
# def send_notif_sms(phone, adcode):
# 	try:
# 		api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')
		
# 		params = {
# 			'sender': '2000660110', #optional
# 			'template': 'notif',
# 			'receptor': 9012994672, #multiple mobile number, split by comma
# 			'type': 'sms',
# 			'token': adcode,
# 		}
# 		response = api.verify_lookup(params)
# 	except APIException as e:
# 		print(e)
# 	except HTTPException as e:
# 		print(e)
# # corns 

# from django.utils.timezone import now, timedelta

# from .models import OtpCode
# # from .utils import send_notif_sms

# # Delete Useless OtpCode
# def delete_useless_otp_code():

# 	"""
# 		Delete useless code in otp_code table
# 		This function will be called every 5 minutes
# 		Call this function in the settings.py file
# 	"""
# 	print('ok')
# 	expired_date = now() - timedelta(minutes=5)
# 	OtpCode.objects.filter(request_date__lt=expired_date).delete()
	
# # fonction

# from rest_framework.validators import ValidationError
# from django.utils.crypto import get_random_string
# from rest_framework.response import Response
# from rest_framework import status
# import random
# from rest_framework.authentication import SessionAuthentication

# from dashbord.models import OtpCode



# from .utils import send_otp_code


# # ? Create hash token
# def create_hash_token():
#     """
#             Generate a random string of 25 characters
#             This will be used as the hash token for the OTP code 
#     """
#     hash_str = "000005fab4534d05api_key9a0554259914a86fb9e7eb014e4e5d52permswrite"
#     hash_str = ("".join(random.sample(hash_str, 25)))
#     return hash_str


# def create_otp_code(request, phone, token):
#     """
#             Create a code for sms verification
#     """
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip_address = x_forwarded_for.split(',')[-1].strip()
#         return Response({'detail': "وی پی ان خود را قطع کنید سپس وارد شوید", 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
#     else:
#         ip_address = request.META.get('REMOTE_ADDR')

#     # check_ip = OtpCode.objects.filter(ip_address=ip_address)
#     random_code = get_random_string(length=4, allowed_chars='1234567890')

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

#     otp_code = OtpCode.objects.create(
#         phone=phone, token=token, code=random_code, ip_address=ip_address)
#     send_otp_code(phone, random_code)
#     return otp_code

# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         return
	
# # Authentiction\

# from rest_framework.response import Response
# from rest_framework import exceptions
# import jwt
# import datetime
# from .models import User
# from django.conf import settings

# # Secret key should be set in your settings.py
# SECRET_KEY = settings.SECRET_KEY

# # Create token
# def create_refresh_token(id, fullname, phone):
#     return jwt.encode({
#         'phone': phone,
#         'user_id': id,
#         'fullname': fullname,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=90),
#     }, SECRET_KEY, algorithm='HS256')

# # Decode refresh token
# def decode_refresh_token(token):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         return payload
#     except jwt.ExpiredSignatureError:
#         raise exceptions.AuthenticationFailed('Token has expired')
#     except jwt.InvalidTokenError:
#         raise exceptions.AuthenticationFailed('Invalid token')

# # Set Cookie
# def set_cookie_for_user(request, refresh_token):
#     response = Response()
#     # current_site = Site.objects.get_current()
#     # current_site = f".{current_site.domain}"
#     response.set_cookie(
#         key='Authorization',
#         value=refresh_token,
#         httponly=True,
#         samesite='None',
#         expires=datetime.datetime.utcnow() + datetime.timedelta(days=91)  # Update domain for production
#     )
#     return response

# # Get user by JWT token
# def get_user_by_token(request):
#     refresh_token = request.COOKIES.get('Authorization')
#     if refresh_token:
#         refresh_decode = decode_refresh_token(refresh_token)
#         user = User.objects.filter(phone=refresh_decode['phone']).first()
#         return user
    
#     return None  # Explicitly returning None if no token is found
# # Admin
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import OtpCode


# class OtpCodeAdmin(admin.ModelAdmin):
# 	list_display = ('phone', 'code', 'ip_address')
# 	list_filter =  ('phone',)
# 	readonly_fields = ('request_date',)
# admin.site.register(OtpCode, OtpCodeAdmin)
