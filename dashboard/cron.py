
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
	
from django.utils.timezone import now, timedelta

from .models import OtpCode

# Delete Useless OtpCode
def delete_useless_otp_code():

	"""
		Delete useless code in otp_code table
		This function will be called every 5 minutes
		Call this function in the settings.py file
	"""
	print('ok')
	expired_date = now() - timedelta(minutes=5)
	OtpCode.objects.filter(request_date__lt=expired_date).delete()

