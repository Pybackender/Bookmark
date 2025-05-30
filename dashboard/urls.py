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

]
