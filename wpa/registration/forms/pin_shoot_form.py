import logging

from django import forms
from django.forms import ModelForm, TextInput, Select
from registration.models import Pin_shoot

logger = logging.getLogger(__name__)


class PinShootForm(ModelForm):
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
               'class': "form-control m-2 email"}))
    email.required = True
    club = forms.CharField(required=False, widget=TextInput(attrs={'placeholder': 'Club', 'autocomplete': 'off',
                                                                   'class': "form-control m-2"}))
    wpa_membership_number = forms.CharField(required=False, widget=TextInput(
        attrs={'placeholder': 'WPA Membership Number', 'autocomplete': 'off',
               'class': "form-control m-2"}))

    class Meta:
        model = Pin_shoot
        fields = ['first_name', 'last_name', 'club', 'category', 'bow', 'shoot_date', 'distance', 'target',
                  'prev_stars', 'wpa_membership_number', 'score', 'email']
        widgets = {'first_name': TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                  'class': "form-control m-2 not_empty"}),
                   'last_name': TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                 'class': "form-control m-2 not_empty"}),
                   'category': Select(attrs={'class': "form-control m-2"}),
                   'bow': Select(attrs={'class': "form-control m-2"}),
                   'shoot_date': TextInput(attrs={'append': 'fa fa-calendar', 'icon_toggle': True,
                                                  'class': "form-control date_input"}),
                   'distance': Select(attrs={'class': "form-control m-2"}, choices=((9, 9), (18, 18))),
                   'target': Select(attrs={'class': "form-control m-2"}, choices=((60, 60), (40, 40))),
                   'prev_stars': Select(attrs={'class': "form-control m-2"}),
                   'score': TextInput(attrs={'placeholder': 'Score', 'autocomplete': 'off',
                                             'class': "form-control m-2 numeric", 'required': ""})
                   }

