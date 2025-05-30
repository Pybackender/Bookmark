# # import random
# # from kavenegar import KavenegarAPI

# # def generate_random_otp(length=4):
# #     """تولید یک کد OTP تصادفی با طول مشخص"""
# #     return ''.join(random.choices('0123456789', k=length))

# # def send_otp_code(phone):
# #     otp = generate_random_otp()  # تولید کد OTP تصادفی
# #     api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')  # کلید API خود را جایگزین کنید
    
# #     # پارامترهای ارسال پیامک
# #     params = {
# #         'sender': '2000660110',  # شماره فرستنده (مطمئن شوید که این شماره معتبر است)
# #         'receptor': phone,        # شماره گیرنده
# #         'message': f'کد تایید شما: {otp}'  # پیام شامل کد OTP
# #     }
    
# #     try:
# #         response = api.sms_send(params)  # ارسال پیامک
# #         print(f"OTP {otp} sent to {phone}. Response: {response}")
# #     except Exception as e:
# #         print(f"Failed to send OTP. Error: {str(e)}")

# # send_otp_code('09012994672')
# # ##############################################
# import random
# from kavenegar import KavenegarAPI

# # from dashboard.views import VerifyCodeView

# # def generate_random_otp(length=4):
# #     """تولید یک کد OTP تصادفی با طول مشخص"""
# #     return ''.join(random.choices('0123456789', k=length))

# # def send_otp_code(phone):
# #     otp = generate_random_otp()  # تولید کد OTP تصادفی
# #     print(f"Generated OTP: {otp}")  # چاپ کد OTP در ترمینال
# #     api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')  # کلید API خود را جایگزین کنید
    
# #     # پارامترهای ارسال پیامک
# #     params = {
# #         'sender': '2000660110',  # شماره فرستنده (مطمئن شوید که این شماره معتبر است)
# #         'receptor': phone,        # شماره گیرنده
# #         'message': f'کد تایید شما: {otp}'  # پیام شامل کد OTP
# #     }
    
# #     try:
# #         response = api.sms_send(params)  # ارسال پیامک
# #         print(f"OTP {otp} sent to {phone}. Response: {response}")
# #     except Exception as e:
# #         print(f"Failed to send OTP. Error: {str(e)}")

# # send_otp_code('09012994672')

# #################################################

# def generate_random_otp(length=4):
#     """تولید یک کد OTP تصادفی با طول مشخص"""
#     return ''.join(random.choices('0123456789', k=length))
# def send_otp_code(phone, otp_storage):
#     otp = generate_random_otp()  # تولید کد OTP تصادفی
#     print(f"Generated OTP: {otp}")  # چاپ کد OTP در ترمینال
#     api = KavenegarAPI('335942696D48734C5572766470584846416E7679456B6332356D686B517658433255356C7073466F35574D3D')  # کلید API خود را جایگزین کنید
    
#     # ذخیره کد OTP در دیکشنری
#     otp_storage[phone] = otp

#     # پارامترهای ارسال پیامک
#     params = {
#         'sender': '2000660110',  # شماره فرستنده
#         'receptor': phone,        # شماره گیرنده
#         'message': f'کد تایید شما: {otp}'  # پیام شامل کد OTP
#     }
    
#     try:
#         response = api.sms_send(params)  # ارسال پیامک
#         print(f"OTP {otp} sent to {phone}. Response: {response}")
#     except Exception as e:
#         print(f"Failed to send OTP. Error: {str(e)}")

from kavenegar import *



def send_otp_code(phone, code):
	#? send sms to user
	# try:
	# 	api = KavenegarAPI('77686E5066454669436B623944624A536C58334F32345055356E6E4543363175482F6B35313748617566733D')
		
	# 	params = {
	# 		'sender': '', #optional
	# 		'template': 'otp',
	# 		'receptor': phone, #multiple mobile number, split by comma
	# 		'token': code,
	# 		'type': 'sms'
	# 	}
	# 	response = api.verify_lookup(params)
	# 	print(response)
	# except APIException as e:
	# 	print(e)
	# except HTTPException as e:
	# 	print(e)
	pass

#TODO about payment sms
def send_notif_sms(phone, adcode):
	try:
		api = KavenegarAPI('77686E5066454669436B623944624A536C58334F32345055356E6E4543363175482F6B35313748617566733D')
		
		params = {
			'sender': '', #optional
			'template': 'notif',
			'receptor': phone, #multiple mobile number, split by comma
			'type': 'sms',
			'token': adcode,
		}
		response = api.verify_lookup(params)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)