from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *


app_name = 'registration'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('email_verify', VerifyEmailView.as_view(), name='email_verify'),
    path('joad_registration/', JoadRegistrationView.as_view(), name='joad_registration'),
    path('joad_session/', JoadSessionView.as_view(), name='joad_session'),
    path('login/', LoginView.as_view(), name='login'),
    path('member_list/', MemberListView.as_view(), name='member_list'),
    path('message/', MessageView.as_view(), name='message'),
    path('pin_shoot/', PinShootView.as_view(), name='pin_shoot'),
    path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    path('register/', RegisterView.as_view(), name='register'),
    path('renew_code/', RenewCodeView.as_view(), name='renew_code'),
    path('renew_membership/', RenewMembershipView.as_view(), name='renew_membership')
]
