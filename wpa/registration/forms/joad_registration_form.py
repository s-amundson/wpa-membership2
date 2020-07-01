import logging

from django import forms
from django.forms import ModelForm, TextInput, Select, CheckboxInput
from registration.models import Joad_session_registration
from .joad_sessions_form import joad_sessions
logger = logging.getLogger(__name__)


class JoadRegistrationForm(ModelForm):
    first_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                         'class': "form-control m-2 not_empty"}), required=True)

    last_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                        'class': "form-control m-2 not_empty"}), required=True)

    email = forms.EmailField(widget=TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
                                                     'class': "form-control m-2 email"}))

    joad = forms.ChoiceField(choices=joad_sessions(), widget=Select(attrs={'class': "form-control m-2"}))

    terms = forms.BooleanField(widget=CheckboxInput(attrs={'class': "form-control m-2 custom-control-input"}),
                               required=True)

    class Meta:
        model = Joad_session_registration
        fields = ['first_name', 'last_name', 'email', 'joad', 'terms']

