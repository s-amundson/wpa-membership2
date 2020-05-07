from django.urls import path

from registration import views
app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),
    path('cost_values/', views.cost_values, name='cost_values'),
    path('fam_done/', views.message, name='fam_done'),
    path('message/', views.message, name='message'),
    path('reg_values/', views.reg_values, name='reg_values'),
    path('register/', views.register, name='register'),
    path('dev/', views.dev, name='dev')
]