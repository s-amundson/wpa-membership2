import logging
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db.models import Max
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.datetime_safe import date, datetime
from django.views import View

from registration.forms import MemberForm, MemberFormSet
from registration.models import Membership, Joad_session_registration, Joad_sessions
from registration.src.Email import Email
from registration.views_function import costs  # todo.txt make costs a table

logger = logging.getLogger(__name__)


class RegisterFormsetView(View):
    # to initalize with data initial = dict of data

    def get(self, request):
        formset = MemberFormSet
        return render(request, 'registration/regform.html', {'formset': formset})

    # elif request.method == "POST":
    def post(self, request):
        formset = MemberFormSet(request.POST)

        form = MemberForm(request.POST)
        j = request.POST.get('joad', None)
        if j is not None:
            form.fields['joad'].choices = [(j, j)]
            logging.debug(j)
            d = request.POST.get('dob', None)
            if d is None or not Joad_session_registration.joad_check_date(date.fromisoformat(d)):
                return render(request, 'registration/message.html', {'message': 'Error on form.'})
        if form.is_valid():
            logging.debug(form.cleaned_data)
            # check for duplicate
            member = form.save(commit=False)
            if member.check_duplicate(form.cleaned_data):
                return render(request, 'registration/message.html', {'message': 'Duplicate found'})
            member.reg_date = member.exp_date = datetime.now()
            member.verification_code = request.session.get('verification_code', str(uuid4()))
            member.status = 'new'
            member.save()

            logging.debug(f"member.level = {member.level}")
            if member.level == 'family':
                if request.session.get('fam_id', None) is None:
                    # new family gets a new family id.
                    f = Membership.objects.all().aggregate(Max('fam_id'))
                    if f['fam_id__max'] is None:
                        f['fam_id__max'] = 0
                    request.session['fam_id'] = f['fam_id__max'] + 1
                    request.session['family_total'] = costs['family_membership']
                    request.session['verification_code'] = member.verification_code
                    fam_reg = request.POST.copy()
                    fam_reg['first_name'] = fam_reg['last_name'] = fam_reg['dob'] = ''
                    request.session['fam_reg'] = fam_reg
                member.fam = request.session['fam_id']
                member.save()

                # logging.debug(f"fam_id = {request.session['fam_id']}, family_total = {request.session['family_total']}")
                Membership.objects.create(fam_id=request.session['fam_id'], member=member)
                # return HttpResponseRedirect(reverse('registration:register'))

            # Joad will either be 'None' or None if no session is selected.
            if 'joad' in request.POST:
                # logging.debug(request.POST['joad'])
                joad = request.POST['joad']
                if joad == "None":
                    joad = None

                # If a JOAD session was selected, check that the member is under 21,
                # if so register them for a session.
                if joad is not None:
                    logging.debug(joad)
                    try:
                        js = Joad_sessions.objects.get(start_date=joad)
                        Joad_session_registration.objects.create(mem=member, pay_status=member.status,
                                                                 idempotency_key=member.verification_code, session=js)
                    except ValidationError as e:
                        logging.error(f"Registration error with joad: {e}")
                    if 'family_total' in request.session:
                        # this error occured after selecting a joad session and then selecting none
                        request.session['family_total'] += costs['joad_session']

            else:
                joad = None
                logging.debug("joad not in request.POST")

            if member.level != 'family':
                # Clear the session for the next user
                request.session.flush()
                Email.verification_email(model_to_dict(member))

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

        else:
            logging.debug("invalid form")
            # logging.debug(form.cleaned_data)
            # logging.debug(form.errors)

        return HttpResponseRedirect(reverse('registration:register'))
    # else:
    #     raise Http404('Register Error')