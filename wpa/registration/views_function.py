import logging
import os
import uuid

from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime, date
from django.forms.models import model_to_dict

from registration.forms import MemberForm, PinShootForm
from registration.models import Joad_sessions, Member, Family, Joad_session_registration, Pin_scores
from registration.src.Email import Email


project_directory = os.path.dirname(os.path.realpath(__file__))

costs = {'standard_membership': 20,
         'family_membership': 40,
         'joad_membership': 18,
         'senior_membership': 18,
         'benefactor': 100,
         'joad_session': 95,
         'pin_shoot': 15,
         'joad_pin': 5,
         'family_total': None}


logger = logging.getLogger(__name__)


def cost_values(request):
    if request.method == "GET":

        # TODO add family total
        costs['family_total'] = None  # session.get('family_total', None)
        return JsonResponse(costs)

    else:
        raise Http404('Cost Values Error')


def dev(request):
    if request.method == "GET":
        form = MemberForm()
        form.first_name = "Joe"
        # return render(request, 'registration/regform.html', {'form': form})
        # return HttpResponseRedirect(reverse('registration:register'), message_text="Form Error")
        # return redirect('registration:register', message_text="Form Error")
        # return redirect('/register/', message_text="Form Error")
        # form = FamilyForm()
        title = "Family Form"
        # return render(request, 'registration/general_form.html', {'title': title, 'title1': title, 'form': form})
        return render(request, 'registration/datepicker.html', {'form': form})

    elif request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            logging.debug('valid form')
            member = form.save(commit=False)
            member.reg_date = member.exp_date = datetime.now()
            member.email_code = str(uuid.uuid4())
            member.status = 'new'
            member.save()
            return HttpResponseRedirect(reverse('registration:dev'))
        else:
            logging.debug('invalid form')
            return render(request, 'registration/message.html', {'message': 'invalid form'})

    else:
        raise Http404('Register Error')


def fam_done(request):
    try:
        member = Member.objects.filter(fam=request.session['fam'])
        if len(member > 0):
            Email.verification_email(model_to_dict(member[0]))
            request.session.flush()
            return render(request, 'registration/message.html', {'message': 'Family Registration complete'})
    except Member.DoesNotExist:
        request.session.flush()
        return render(request, 'registration/message.html', {'message': 'Error with family or session'})


def index(request):
    return render(request, 'registration/index.html')


def message(request, text=""):
    return render(request, 'registration/message.html', {'message': text})
