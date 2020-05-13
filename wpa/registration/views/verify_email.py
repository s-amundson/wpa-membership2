from django.shortcuts import render
from django.views import View

from forms import EmailValidate, MemberForm
from registration.models import Member


class VerifyEmailView(View):
    def get(self, request):
        email = request.GET.get('e', '')
        vcode = request.GET.get('c', '')
        form = EmailValidate(initial={'email': email, 'verification_code': vcode})
        return render(request, 'registration/email_verify.html', {'form': form})

    def post(self, request):
        form = MemberForm(request.POST)
        if form.is_valid():
            rows = Member.objects.filter(email=form.cleaned_data['email'],
                                         verification_code=form.cleaned_data['verification_code'])
            if rows > 0:
                # TODO process payment.
                pass
        # else:
        return render(request, 'registration/message.html', {'message': 'Error on form.'})