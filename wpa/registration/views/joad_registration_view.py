import logging
from uuid import uuid4

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import View

from forms import JoadRegistrationForm

from registration.models import Joad_sessions, Member

logger = logging.getLogger(__name__)


class JoadRegistrationView(View):
    def get(self, request):
        form = JoadRegistrationForm
        context = {'form': form}
        return render(request, 'registration/joad_registration.html', context)

    def post(self, request):
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
            if not reg.joad_check_date(member[0].dob):
                return render(request, 'registration/message.html', {'message': 'Student is over 21'})
            reg.mem = member[0]
            reg.pay_status = 'new'
            reg.idempotency_key = str(uuid4())

            reg.session = Joad_sessions.objects.filter(start_date=reg_data['joad'])[0]
            reg.save()
            return HttpResponseRedirect(reverse('registration:pin_shoot'))
        logging.debug(form.errors)
        return render(request, 'registration/message.html', {'message': 'Error on form.'})
