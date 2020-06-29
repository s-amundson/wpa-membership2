import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from registration.forms import JoadSessionForm

logger = logging.getLogger(__name__)



class JoadSessionView(LoginRequiredMixin, View):
    """Shows a message page"""

    def get(self, request):
        form = JoadSessionForm()
        return render(request, 'registration/joad_session.html', {'form': form})

    def post(self, request):
        form = JoadSessionForm(request.POST)
        j = request.POST.get('state', None)
        if j is not None:
            form.fields['state'].choices = [(j, j)]
        if form.is_valid():
            js = form.save()
            logging.debug('valid ' + js.start_date.isoformat())
        else:
            logging.debug(form.errors)
        return redirect('registration:joad_session')
