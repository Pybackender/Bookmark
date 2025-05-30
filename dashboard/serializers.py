# from rest_framework import serializers
# from .models import OtpCode

# class OtpCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OtpCode
#         fields = ['id', 'phone', 'ip_address', 'code', 'token', 'request_date']
#         read_only_fields = ['id', 'request_date']  # Make these fields read-only

#     def validate_code(self, value):
#         """
#         Check that the code is a positive integer.
#         """
#         if value <= 0:
#             raise serializers.ValidationError(_("Code must be a positive integer."))
#         return value

#     def validate_phone(self, value):
#         """
#         Check that the phone number is valid.
#         """
#         if len(value) != 11 or not value.isdigit():
#             raise serializers.ValidationError(_("Phone number must be 11 digits."))
#         return value



from rest_framework import serializers

from .models import City, Role, Company, Province



class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
	ad_count = serializers.SerializerMethodField()
	province = serializers.SerializerMethodField()

	def get_province(self, obj):
		data = {
			"id": obj.province.id,
			"name": obj.province.name,
			"slug": obj.province.slug,
		}
		return data

	class Meta:
		model = City
		fields = "__all__"


class ProvinceSerializer(serializers.ModelSerializer):

	class Meta:
		model = Province
		fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
	phone = serializers.SerializerMethodField()

	def get_phone(self, obj):
		return obj.owner.phone
	
	class Meta:
		model = Company
		fields = "__all__"
