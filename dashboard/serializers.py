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
