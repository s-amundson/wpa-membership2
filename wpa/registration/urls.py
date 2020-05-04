from django.urls import path

from . import views
app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),
    path('cost_values/', views.cost_values, name='cost_values'),
    path('fam_done/', views.message, name='fam_done'),
    path('message/', views.message, name='message'),
    path('register/', views.register, name='register'),
    path('regform/', views.regform, name='regform')
]