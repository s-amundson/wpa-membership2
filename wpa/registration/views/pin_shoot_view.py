import logging

from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.base import View

from forms import PinShootForm
from square_helper import line_item

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
            shoot.save()
            stars_earned = shoot.stars - shoot.prev_stars
            fields = ['first_name', 'last_name', 'club', 'category', 'bow', 'shoot_date', 'distance', 'target',
                      'prev_stars', 'wpa_membership_number', 'score']
            l = [line_item(f"JOAD Pin Shoot {request.POST['shoot_date']}", 1, 15),
                 line_item(f"JOAD Pins {request.POST['shoot_date']}", stars_earned, 5)]
            logging.debug(f"line items = {l}")
            request.session['line_items'] = l
            request.session['email'] = form.cleaned_data.get('email', '')

            return HttpResponseRedirect(reverse('registration:pin_shoot'))
        else:
            logging.debug(form.errors)
            return render(request, 'registration/message.html', {'message': 'Error on form.'})
