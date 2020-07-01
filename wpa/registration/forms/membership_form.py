import logging

from django import forms
from django.forms import ModelForm, TextInput, Select, CheckboxInput, inlineformset_factory
from registration.models import Member, Membership
from . import MemberForm

logger = logging.getLogger(__name__)


MembershipFormSet = inlineformset_factory(Membership, Member, form=MemberForm, can_delete=True, extra=0, min_num=0,
                                          max_num=4)


class MembershipForm(ModelForm):
    terms = forms.BooleanField(widget=CheckboxInput(attrs={'class': "form-control m-2 custom-control-input"}),
                               required=True)

    class Meta:
        model = Membership
        fields = ['street', 'city', "state", "post_code", "phone", "email", "level", "benefactor", 'terms']
        widgets = {'street': TextInput(attrs={'placeholder': 'Street', 'autocomplete': 'off',
                                              'class': "form-control m-2 not_empty"}),
                   'city': TextInput(attrs={'placeholder': 'City', 'autocomplete': 'off',
                                            'class': "form-control m-2 not_empty"}),
                   'state': TextInput(attrs={'placeholder': 'State', 'autocomplete': 'off',
                                             'class': "form-control m-2 not_empty"}),
                   'post_code': TextInput(attrs={'placeholder': 'Zip', 'autocomplete': 'off',
                                                 'class': "form-control m-2 not_empty"}),
                   'phone': TextInput(attrs={'placeholder': 'Phone', 'autocomplete': 'off',
                                             'class': "form-control m-2 not_empty"}),
                   'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off',
                                             'class': "form-control m-2 email"}),
                   'level': Select(attrs={'class': "form-control m-2 costs "}),
                   'benefactor': CheckboxInput(attrs={'class': "form-control m-2 custom-control-input costs"})
                   }
