from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from .forms import UserCreationForm, UserChangeForm
from .models import *


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm

	list_display = ('fullname', 'phone','role', 'status')
	list_filter =  ('role',)
	fieldsets = (None, {'fields': ('fullname','password','phone', 'email', 'role','avatar', 'status', 'last_login','date_joined' )}),
	readonly_fields= ('last_login','date_joined')
	add_fieldsets = (None, {'fields': ('fullname' ,'phone','email', 'role','status','password1', 'password2')}),

	search_fields =  ('fullname', 'email')
	ordering = ('fullname',)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)


class OtpCodeAdmin(admin.ModelAdmin):
	list_display = ('phone', 'code', 'ip_address')
	list_filter =  ('phone',)
	readonly_fields = ('request_date',)
admin.site.register(OtpCode, OtpCodeAdmin)


class RoleAdmin(admin.ModelAdmin):
	list_display = ('name', 'display_name')
	list_filter =  ('name',)
	search_fields =  ('name',)
	ordering = ('name',)
admin.site.register(Role, RoleAdmin)

class MediaUserAdmin(admin.ModelAdmin):
	list_display = ('user', 'file', 'subject_type')
	list_filter =  ('user',)
	search_fields =  ('id',)
	ordering = ('user',)
admin.site.register(MediaUser, MediaUserAdmin)
