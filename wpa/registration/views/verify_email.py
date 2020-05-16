import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from registration.forms import EmailValidate, MemberForm
from registration.models import Member, Joad_session_registration
from registration.src.square_helper import line_item

logger = logging.getLogger(__name__)

class VerifyEmailView(View):
    def get(self, request):
        email = request.GET.get('e', '')
        vcode = request.GET.get('c', '')
        form = EmailValidate(initial={'email': email, 'email_code': vcode})
        return render(request, 'registration/email_verify.html', {'form': form})

    def post(self, request):
        form = EmailValidate(request.POST)
        if form.is_valid():
            rows = Member.objects.filter(email=form.cleaned_data['email'],
                                         email_code=form.cleaned_data['email_code'])
            if len(rows) > 0:
                # joad_sessions = 0
                cost = settings.COSTS[f"{rows[0].level}_membership"]
                l = [line_item("Membership", 1, cost)]

                js = Joad_session_registration.objects.filter(idempotency_key=form.cleaned_data['email_code'])
                # if len(rows) == 1:
                #     if rows[0].joad is not None:
                #         joad_sessions += 1
                # else:
                #     for row in rows:
                #         if row.joad is not None:
                #             joad_sessions += 1
                if len(js) > 0:
                    cost = settings.COSTS['joad_session'] * len(js)
                    l.append(line_item(f'Joad Session {rows[0].joad.isoformat()}'), len(js), cost)

                request.session['line_items'] = l
                request.session['idempotency_key'] = form.cleaned_data['email_code']
                return HttpResponseRedirect(reverse('registration:process_payment'))
        else:
            logging.debug(form.errors)
        return render(request, 'registration/message.html', {'message': 'Error with form.'})