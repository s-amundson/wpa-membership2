import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from registration.forms import EmailValidate, MemberForm
from registration.models import Member, Joad_session_registration, Membership
from registration.src.square_helper import line_item

logger = logging.getLogger(__name__)


class VerifyEmailView(View):
    def get(self, request):
        email = request.GET.get('e', '')
        vcode = request.GET.get('c', '')
        form = EmailValidate(initial={'email': email, 'verification_code': vcode})
        return render(request, 'registration/email_verify.html', {'form': form})
        # return render(request, 'registration/message.html', {'message': 'Error with form.'})

    def post(self, request):
        form = EmailValidate(request.POST)
        if form.is_valid() and len(form.cleaned_data['verification_code']) > 12:
            rows = Membership.objects.filter(email=form.cleaned_data['email'],
                                             verification_code__startswith=form.cleaned_data['verification_code'],
                                             status='new')
            # headline__startswith='What'
            logging.debug(form.cleaned_data)
            if len(rows) > 0:
                line_dict = Membership.line_items_from_membership(rows[0])
                for k, v in line_dict.items():
                    request.session[k] = v
                return HttpResponseRedirect(reverse('registration:process_payment'))
        else:
            logging.debug(form.errors)
        return render(request, 'registration/message.html', {'message': 'Error with form.'})
