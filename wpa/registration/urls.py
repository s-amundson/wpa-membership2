from django.urls import path

from registration import views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),

    path('fam_done/', views.message, name='fam_done'),
    path('joad_registration/', views.joad_registration, name='joad_registration'),
    path('message/', views.message, name='message'),
    path('pin_shoot/', views.pin_shoot, name='pin_shoot'),

    path('register/', views.register, name='register'),
    path('dev/', views.dev, name='dev')
]
