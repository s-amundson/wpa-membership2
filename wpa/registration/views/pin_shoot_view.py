import logging

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import View

from forms import PinShootForm

logger = logging.getLogger(__name__)


class PinShootView(View):
    def get(self, request):
        form = PinShootForm
        context = {'form': form}
        return render(request, 'registration/pin_shoot.html', context)

    def post(self, request):
        form = PinShootForm(request.POST)
        selects = ['category', 'bow', 'shoot_date', 'distance', 'target', 'prev_stars']
        for i in selects:
            c = request.POST.get(i, None)
            form.fields[i].choices = [(c, c)]

        if form.is_valid():
            logging.debug(form.cleaned_data)
            shoot = form.save(commit=False)
            if shoot.wpa_membership_number == "":
                shoot.wpa_membership_number = None
            # stars_earned = shoot.stars - shoot.prev_stars
            shoot.save()
            fields = ['first_name', 'last_name', 'club', 'category', 'bow', 'shoot_date', 'distance', 'target',
                      'prev_stars', 'wpa_membership_number', 'score']
            # todo create line items
            return HttpResponseRedirect(reverse('registration:pin_shoot'))
        else:
            logging.debug(form.errors)
            return render(request, 'registration/message.html', {'message': 'Error on form.'})
