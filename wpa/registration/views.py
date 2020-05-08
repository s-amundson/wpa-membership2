import logging
import os
import sys
import uuid

from django.db.models import Max
from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.datetime_safe import datetime, date

from registration.src.joad_helper import calculate_pins, joad_check_date
from registration.forms import FamilyForm, JoadRegistrationForm, MemberForm, PinShootForm
from registration.src.register_helper import check_duplicate
from registration.models import Joad_sessions, Member, Family, Joad_session_registration
from registration.src.Config import Config

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


def joad_registration(request):
    if request.method == "GET":
        form = JoadRegistrationForm
        context = {'form': form}
        return render(request, 'registration/joad_registration.html', context)
    elif request.method == "POST":
        form = JoadRegistrationForm(request.POST)
        j = request.POST.get('joad')
        form.fields['joad'].choices = [(j, j)]
        if form.is_valid():
            logging.debug(form.cleaned_data)
            reg_data = form.cleaned_data
            reg = form.save(commit=False)
            try:
                member = Member.objects.filter(first_name=reg_data['first_name'],
                                               last_name=reg_data['last_name'],
                                               email=reg_data['email'])
            except Member.DoesNotExist:
                return render(request, 'registration/message.html', {'message': 'Member not found'})
            if not joad_check_date(member[0].dob):
                return render(request, 'registration/message.html', {'message': 'Student is over 21'})
            reg.mem = member[0]
            reg.pay_status = 'new'
            reg.idempotency_key = str(uuid.uuid4())

            reg.session = Joad_sessions.objects.filter(start_date=reg_data['joad'])[0]
            reg.save()
            return HttpResponseRedirect(reverse('registration:pin_shoot'))
        logging.debug(form.errors)
        return render(request, 'registration/message.html', {'message': 'Error on form.'})
    else:
        raise Http404('JOAD Register Error')

#     pay_status = models.CharField(max_length=20)
#     email_code = models.CharField(max_length=50, null=True, default=None)
#     session = models.ForeignKey(Joad_sessions, on_delete=models.DO_NOTHING)


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


def pin_shoot(request):
    if request.method == "GET":
        form = PinShootForm
        context = {'form': form}
        return render(request, 'registration/pin_shoot.html', context)

    elif request.method == "POST":
        form = PinShootForm(request.POST)
        if form.is_valid():
            logging.debug(form.cleaned_data)
            shoot = form.save(commit=False)
            if shoot.wpa_membership_number == "":
                shoot.wpa_membership_number = None
            shoot.stars = calculate_pins(form.cleaned_data) - shoot.prev_stars
            if shoot.stars < 0:
                shoot.stars = 0
            shoot.save()
            fields = ['first_name', 'last_name', 'club', 'category', 'bow', 'shoot_date', 'distance', 'target',
                      'prev_stars', 'wpa_membership_number', 'score']
            return HttpResponseRedirect(reverse('registration:pin_shoot'))
    else:
        raise Http404('Pin Shoot Error')


def register(request):
    # to initalize with data initial = dict of data
    form = MemberForm(initial={})
    context = {'form': form, 'costs': costs, 'message': ''}

    if request.method == "GET":
        return render(request, 'registration/register.html', context)

    elif request.method == "POST":
        form = MemberForm(request.POST)
        logging.debug(request.POST)
        j = request.POST.get('joad', None)
        if j is not None:
            form.fields['joad'].choices = [(j, j)]
            logging.debug(j)
            if not joad_check_date(date.fromisoformat(request.POST.get('dob', ""))):
                return render(request, 'registration/message.html', {'message': 'Error on form.'})
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
                    js = Joad_sessions.objects.get(start_date=date.fromisoformat(joad))
                    Joad_session_registration.objects.create(mem=member, pay_status=member.status,
                                                             idempotency_key=member.email_code, session=js)
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


def show_session(session):
    logging.debug(f'show session, len= {len(session.items())}')
    for k,v in session.items():
        logging.debug(f"k = {k} v={v}")
