import json
import logging

from django.conf import settings
from django.db import transaction
from django.forms import model_to_dict, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datetime_safe import date
from django.views.generic import UpdateView
from registration.forms import MembershipFormSet, MemberForm, MembershipForm
from registration.models import Membership, Member, OrphanMember
from registration.views import RegisterView

logger = logging.getLogger(__name__)
# live
# <QueryDict: {'csrfmiddlewaretoken': ['py8devipQ2u86att0f5oYuXhknmtIobAPeLThkx0O2HxaCvmYLHXb2j5nKPRGMlT'],
# 'member_set-TOTAL_FORMS': ['1'], 'member_set-INITIAL_FORMS': ['1'], 'member_set-MIN_NUM_FORMS': ['0'],
# 'member_set-MAX_NUM_FORMS': ['4'], 'member_set-0-id': ['26'], 'member_set-0-first_name': ['Melvin'],
# 'member_set-0-last_name': ['Obrien'], 'member_set-0-dob': ['1977-05-13'], 'member_set-0-joad': [''],
# 'street': ['4385 Carson Street'], 'city': ['San Diego'], 'state': ['CA'], 'post_code': ['92101'],
# 'email': ['MelvinPObrien@fleckens.hu'], 'phone': ['858-879-1341'], 'level': ['standard'], 'terms': ['on']}>

# test
# <QueryDict: {'csrfmiddlewaretoken': ['SQW46AFNMMUdA2MBIRrppw2xImcSwPyiKJr6AWTNy8ZYzrz2puQd4lzIps84GUVp'],
# 'member_set-TOTAL_FORMS': ['1'], 'member_set-INITIAL_FORMS': ['0'], 'member_set-MIN_NUM_FORMS': ['0'],
# 'member_set-MAX_NUM_FORMS': ['1000'], 'member_set-0-first_name': ['Christy'],
# 'member_set-0-last_name': ['Snow'], 'member_set-0-dob': ['1996-09-05'], 'member_set-0-joad': [''],
# 'street': ['2166 Court Street'], 'city': ['Eureka'], 'state': ['MO'], 'post_code': ['63025'],
# 'email': ['ChristyCSnow@gustr.com'], 'phone': ['636-587-0922'], 'level': ['standard'], 'terms': ['on'], 'cost': ['20'], 'member_set-0-id': ['5']}>

class RenewMembershipView(RegisterView):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.costs = json.dumps(settings.COSTS)
    #     self.membership_form = MembershipForm()
    #     self.formset = MembershipFormSet(initial={})
    #     self.message = ''
    #     self.context = {'formset': self.formset, 'costs': self.costs, 'message': self.message,
    #                     'membership_form': self.membership_form}
    def get(self, request):
        email = request.GET.get('e', '')
        vcode = request.GET.get('c', '')
        rows = Membership.objects.filter(email=email,
                                         verification_code__startswith=vcode)
        if len(rows) != 1:
            return render(request, 'registration/message.html', {'message': 'Error with form.'})

        membership = model_to_dict(rows[0])
        logging.debug(membership)
        request.session['membership_id'] = rows[0].id
        self.context['membership_id'] = rows[0].id
        # membershipFormSet = inlineformset_factory(Membership, Member, form=MemberForm, can_delete=True, extra=0,
        #                                           min_num=0, max_num=4)
        self.context['membership_form'] = MembershipForm(instance=rows[0])
        self.context['formset'] = MembershipFormSet(instance=rows[0])
        logging.debug(self.context)
        return render(request, 'registration/register.html', self.context)

    def post(self, request):
        logging.debug(request.POST)

        membership_id = request.session.get('membership_id', None)

        instance = Membership.objects.get(id=membership_id)
        self.membership_form = MembershipForm(request.POST, instance=instance)
        self.formset = MembershipFormSet(request.POST, instance=instance)
        logging.debug(f'members in membership: {len(instance.member_set.all())}')
        try:
            membership = self.process_membership(request, membership_id)
            logging.debug(f'members in membership: {len(membership.member_set.all())}')
            # logging.debug(f'changed members {self.formset.changed_objects}')
            logging.debug(f'deleted members {self.formset.deleted_forms}')
            # logging.debug(f'new members {self.formset.new_objects}')
            # for member in self.formset.deleted_forms:
            #     logging.debug(member.cleaned_data)
            #     m = member.cleaned_data['id']
            #     logging.debug(m.membership)
            for m in self.formset.deleted_objects:
                OrphanMember.objects.create(member_id=m.pk, membership=m.membership.pk, first_name=m.first_name,
                                            last_name=m.last_name,
                                            dob=m.dob, orphan_date=date.today())
                m.delete()


        except ValueError as e:
            logging.error(e.strerror)
            return self.return_form(request)

        line_dict = Membership.line_items_from_membership(membership)
        for k, v in line_dict.items():
            request.session[k] = v
        return HttpResponseRedirect(reverse('registration:process_payment'))