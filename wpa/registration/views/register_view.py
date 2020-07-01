import logging
import json
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.views import View
from django_q.tasks import async_task

from registration.models import Member
from registration.forms import MembershipForm, MembershipFormSet
from registration.models import Joad_session_registration, Joad_sessions
from registration.src.Email import Email


logger = logging.getLogger(__name__)


class RegisterView(View):
    # to initialize with data initial = dict of data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.costs = json.dumps(settings.COSTS)
        self.membership_form = MembershipForm()
        self.formset = MembershipFormSet(initial={})
        self.message = ''
        self.context = {'formset': self.formset, 'costs': self.costs, 'message': self.message,
                        'membership_form': self.membership_form}
        self.email_member = None

    def check_duplicate(self, form_data, membership):
        # check for duplicate
        logging.debug(form_data)

        try:
            reg_mem = Member.objects.filter(first_name=form_data['first_name'],
                                            last_name=form_data['last_name'])
        except Member.DoesNotExist:  # pragma: no cover
            reg_mem = None
        if reg_mem is not None and len(reg_mem) > 0:
            logging.debug(f"Duplicate(s) may exist {reg_mem}, len={len(reg_mem)}")
            col = ["street", "city", "state", "zip", "phone", "email", "dob"]
            for row in reg_mem:

                matches = 0
                if row.membership.street == membership.street:
                    matches += 1
                if row.membership.city == membership.city:
                    matches += 1
                if row.membership.state == membership.state:
                    matches += 1
                if row.membership.post_code == membership.post_code:
                    matches += 1
                if row.membership.phone == membership.phone:
                    matches += 1
                if row.membership.email == membership.email:
                    matches += 1
                if row.dob == form_data['dob']:
                    matches += 1

                if matches >= len(col) - 2:
                    logging.debug('Found Match')
                    return True
        return False

    def get(self, request):
        return render(request, 'registration/register.html', self.context)

    def post(self, request):
        logging.debug(request.POST)
        self.membership_form = MembershipForm(request.POST)
        self.formset = MembershipFormSet(request.POST)

        try:
            membership = self.process_membership(request, None)

        except ValueError as e:
            # logging.error(e.strerror)
            return self.return_form(request)

        mem_dict = model_to_dict(membership)
        mem_dict['verification_code'] = mem_dict['verification_code'][:13]
        for k, v in self.email_member.items():
            mem_dict[k] = v
        # Email.verification_email(mem_dict)
        async_task(Email.verification_email, mem_dict, task_name=mem_dict['email'])
        return HttpResponseRedirect(reverse('registration:register'))

    def return_form(self, request):
        self.context['formset'] = self.formset
        self.context['membership_form'] = self.membership_form
        return render(request, 'registration/register.html', self.context)

    def process_membership(self, request, membership_id):
        with transaction.atomic():
            if self.membership_form.is_valid():
                logging.debug('membership valid')
                membership = self.membership_form.save(commit=False)
                if membership_id is None:
                    membership.reg_date = membership.exp_date = datetime.now()
                    membership.verification_code = str(uuid4())
                    membership.status = 'new'

                membership.save()
            else:
                logging.debug(self.membership_form.errors)
                # self.context['formset'] = MembershipFormSet(initial=request.POST)
                self.context['message'] = 'Error on form'
                raise ValueError('Error on form')


            if self.formset.is_valid():
                logging.debug('valid formset')
                # logging.debug(self.formset.cleaned_data)
                for d in self.formset.cleaned_data:
                    if len(d) > 0:
                        if membership_id is None:
                            if self.check_duplicate(d, membership):
                                Ex = ValueError()
                                Ex.strerror = "Duplicate Found."
                                raise Ex
                        if d['joad'] == '':
                            d['joad'] = None
                        elif not Joad_session_registration.joad_check_date(d['dob']):
                            self.message = 'Error on form'
                            return render(request, 'registration/register.html', self.context)

                obj = self.formset.save(commit=False)

                for form in obj:
                    form.membership = membership
                    form.save()
                    if self.email_member is None:
                        self.email_member = model_to_dict(form)

                    # check if member is in JOAD
                    for d in self.formset.cleaned_data:
                        if len(d) > 0:
                            logging.debug(d['joad'])
                            if d['joad'] is not None:
                                if d['first_name'] == form.first_name and d['last_name'] == form.last_name:
                                    try:
                                        js = Joad_sessions.objects.get(start_date=d['joad'])
                                        Joad_session_registration.add_from_member(form, js)
                                    except ValidationError as e:
                                        logging.error(f"Registration error with joad: {e}")
                                        # this error occured after selecting a joad session and then selecting none
            else:
                logging.debug(self.formset.errors)
                self.message = 'Error on form'
                raise ValueError('Error on form')
                # return render(request, 'registration/register.html', self.context)
        return membership
