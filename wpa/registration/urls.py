from django.urls import path

from registration import views_function
from .views import JoadRegistrationView, PinShootView, ProcessPaymentView, RegisterView, VerifyEmailView

app_name = 'registration'
urlpatterns = [
    path('', views_function.index, name='index'),
    path('cost_values/', views_function.cost_values, name='cost_values'),
    path('dev/', views_function.dev, name='dev'),
    path('email_verify', VerifyEmailView.as_view(), name='email_verify'),
    path('fam_done/', views_function.message, name='fam_done'),
    path('joad_registration/', JoadRegistrationView.as_view(), name='joad_registration'),
    path('message/', views_function.message, name='message'),
    path('pin_shoot/', PinShootView.as_view(), name='pin_shoot'),
    path('process_payment/', ProcessPaymentView.as_view(), name='process_payment'),
    path('register/', RegisterView.as_view(), name='register'),
]
