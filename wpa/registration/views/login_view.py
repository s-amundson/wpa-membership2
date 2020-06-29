from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View


class LoginView(View):
    """Shows a login page"""
    def get(self, request):
        return redirect('/registration/accounts/login/')

    # def get(self, request):
    #     return render(request, 'registration/login.html', {})
    #
    # def post(self, request):
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return HttpResponseRedirect(reverse('registration:register'))
    #     else:
    #         return render(request, 'registration/message.html', {'message': 'payment successful'})