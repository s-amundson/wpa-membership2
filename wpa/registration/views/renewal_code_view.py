import logging

from django.conf import settings
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from registration.forms import EmailValidate
from registration.models import Joad_session_registration, Membership
from registration.src.square_helper import line_item
from registration.views import MessageView

logger = logging.getLogger(__name__)


class RenewCodeView(View):
    def get(self, request):
        email = request.GET.get('e', '')
        vcode = request.GET.get('c', '')
        form = EmailValidate(initial={'email': email, 'verification_code': vcode})
        return render(request, 'registration/renew_code.html', {'form': form})
        # return render(request, 'registration/message.html', {'message': 'Error with form.'})

    def post(self, request):
        form = EmailValidate(request.POST)
        if form.is_valid() and len(form.cleaned_data['verification_code']) > 12:
            rows = Membership.objects.filter(email=form.cleaned_data['email'],
                                             verification_code__startswith=form.cleaned_data['verification_code'])
            # headline__startswith='What'
            logging.debug(form.cleaned_data)
            if len(rows) > 0:
                # joad_sessions = 0
                benefactor = False
                for row in rows:
                    ik = row.verification_code
                    if row.status != 'new':
                        # request.session['membership'] = model_to_dict(row)
                        request.session['membership_id'] = row.id
                        logging.debug(request.session['membership_id'])
                        # /renew_code?e={{ email }}&c={{ verification_code }}
                        s = reverse('registration:renew_membership')
                        e = form.cleaned_data['email']
                        c = form.cleaned_data['verification_code']
                        return HttpResponseRedirect(f"{s}?e={e}&c={c}")

                #     if row.benefactor:
                #         benefactor = True
                #
                # if benefactor:
                #     cost = settings.COSTS['benefactor']
                #     lines = [line_item("Benefactor Membership", 1, cost)]
                # else:
                #     cost = settings.COSTS[f"{rows[0].level}_membership"]
                #     lines = [line_item("Membership", 1, cost)]
                #
                # js = Joad_session_registration.objects.filter(idempotency_key=ik, pay_status='new')
                # if len(js) > 0:
                #     logging.debug(js[0].session)
                #     cost = settings.COSTS['joad_session']
                #     lines.append(line_item(f'Joad Session {js[0].session.start_date.isoformat()}', len(js), cost))
                #     logging.debug(lines)
                #
                # request.session['line_items'] = lines
                # request.session['idempotency_key'] = ik
                # return HttpResponseRedirect(reverse('registration:process_payment'))
        else:
            logging.debug(form.errors)
            logging.debug(reverse('registration:message'))
        return render(request, 'registration/message.html', {'message': 'Error with form.'})

