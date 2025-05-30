# from django.urls import path
# from .views import DashboardView, VerifyCodeView
# # from django.views.generic import TemplateView
# from .views import VerifyCodeView


# urlpatterns = [
#     path('', DashboardView.as_view(), name='dashboard'),
#     path('otp-form/', VerifyCodeView.as_view(), name='otp_form'),
#     path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
# ]



from django.urls import path, include
from rest_framework import routers

from .views import  *



app_name = "dashboard"
router = routers.SimpleRouter()

urlpatterns = [
    path('', include(router.urls)),

    path('auth', CheckPhoneView.as_view(), name='auth'),
    path('info', AuthenticatedView.as_view(), name='info'),
    path('verify', VerifyCodeView.as_view(), name='verify'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('password', CheckPasswordView.as_view(), name='password'),
    path('forgot-pass', ForgotPasswordView.as_view(), name='forgot_pass'),
    
    path('user', UserView.as_view(), name='user'),
    path('role', RoleView.as_view(), name='role'),
    path('city', CityView.as_view(), name='city'),
    path('company', CompanyView.as_view(), name='company'),

]
