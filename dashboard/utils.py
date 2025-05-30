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