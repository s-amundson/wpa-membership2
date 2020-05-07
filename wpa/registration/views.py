import logging
import os
import sys
import uuid

from django.db.models import Max
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime, date

from registration.forms import FamilyForm, MemberForm
from src.register_helper import check_duplicate
from .models import Joad_sessions, Member, Family, Joad_session_registration
from .src.Config import Config

# Create your views here.
project_directory = os.path.dirname(os.path.realpath(__file__))
if sys.platform == 'win32':
    # print('windblows')
    cfg = Config('\\'.join(project_directory.split('\\')[:-1]))
    # costs = {}
else:
    cfg = Config('/'.join(project_directory.split('/')[:-1]))

costs = cfg.get_costs()

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'registration/index.html')


def fam_done(request):
    request.session.flush()
    return render(request, 'registration/message.html', {'message': 'Family Registration complete'})


def message(request, text=""):
    return render(request, 'registration/message.html', {'message': text})


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


def reg_values(request):
    if request.method == "GET":
        return JsonResponse(request.session.get('fam_reg', {}))
    else:
        raise Http404('reg_values Error')


def register(request):
    # to initalize with data initial = dict of data
    form = MemberForm(initial={})
    context = {'form': form, 'costs': costs, 'message': ''}

    if request.method == "GET":
        return render(request, 'registration/register.html', context)

    elif request.method == "POST":
        form = MemberForm(request.POST)
        logging.debug(request.POST)
        if form.is_valid():
            logging.debug(form.cleaned_data)
            # check for duplicate
            if check_duplicate(form.cleaned_data):
                return render(request, 'registration/message.html', {'message': 'Duplicate found'})
            member = form.save(commit=False)
            member.reg_date = member.exp_date = datetime.now()
            member.email_code = str(uuid.uuid4())
            member.status = 'new'
            member.save()

            logging.debug(f"member.level = {member.level}")
            if member.level == 'family':
                if request.session.get('fam_id', None) is None:
                    # new family gets a new family id.
                    f = Family.objects.all().aggregate(Max('fam_id'))
                    if f['fam_id__max'] is None:
                        f['fam_id__max'] = 0
                    request.session['fam_id'] = f['fam_id__max'] + 1
                    request.session['family_total'] = costs['family_membership']
                    fam_reg  = request.POST.copy()
                    fam_reg['first_name'] = fam_reg['last_name'] = fam_reg['dob'] = ''
                    request.session['fam_reg'] = fam_reg
                member.fam = request.session['fam_id']
                member.save()

                logging.debug(f"fam_id = {request.session['fam_id']}, family_total = {request.session['family_total']}")
                Family.objects.create(fam_id=request.session['fam_id'], member=member)
                # return HttpResponseRedirect(reverse('registration:register'))

            # Joad will either be 'None' or None if no session is selected.
            if 'joad' in request.POST:
                logging.debug(request.POST['joad'])
                joad = request.POST['joad']
                if joad == "None":
                    joad = None

                # If a JOAD session was selected, check that the member is under 21,
                # if so register them for a session.
                if joad is not None:
                    d = request.POST['dob'].split('-')
                    if date(int(d[0]) + 21, int(d[1]), int(d[2])) > date.today():  # student is not to old.
                        logging.debug("student is not to old.")
                        js = Joad_sessions.objects.get(start_date=date.fromisoformat(joad))
                        Joad_session_registration.objects.create(mem=member, pay_status=member.status,
                                                                 email_code=member.email_code, session=js)
                        if 'family_total' in request.session:
                            request.session['family_total'] += costs['joad']

            else:
                joad = None
                logging.debug("joad not in request.POST")

            if member.level != 'family':
                # Clear the session for the next user
                show_session(request.session)
                request.session.flush()
                show_session(request.session)

                # if (family.fam_id is None):  # not a family registration
                #     session['registration'] = None
                #     # return redirect("/")
                #     return render_template('message.html', message='Registration Done')
            else:  # Family registration


                # Calculate the running cost for the membership with the possibility of adding JOAD sessions in.
                # costs = cfg.get_costs()
                if request.session.get('family_total', None) is None:
                    request.session['family_total'] = costs['family_membership']
                if joad is not None:
                    request.session['family_total'] = request.session['family_total'] + costs['joad_session']
                    request.session['joad_session'] = joad
                costs['family_total'] = request.session['family_total']
                initial = form.cleaned_data.copy()
                keys = ['first_name', 'last_name', 'dob', 'joad', 'terms']
                for k in keys:
                    initial.pop(k, None)
                form = MemberForm(initial=initial)
                context = {'form': form, 'costs': costs, 'message': ''}

                return render(request, 'registration/register.html', context)

                # return render_template("register.html", rows=family.members, joad_sessions=jsdb.list_open())
            # else:
            #     return render_template("register.html", rows=family.members, joad_sessions=jsdb.list_open())
        else:
            logging.debug("invalid form")
            logging.debug(form.cleaned_data)
            logging.debug(form.errors)







        return HttpResponseRedirect(reverse('registration:register'))
    else:
        raise Http404('Register Error')


def cost_values(request):
    if request.method == "GET":

        # TODO add family total
        costs['family_total'] = None  # session.get('family_total', None)
        return JsonResponse(costs)

    else:
        raise Http404('Cost Values Error')


def show_session(session):
    logging.debug(f'show session, len= {len(session.items())}')
    for k,v in session.items():
        logging.debug(f"k = {k} v={v}")
