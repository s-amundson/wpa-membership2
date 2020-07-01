import logging

from django.db import OperationalError
from django.forms import ModelForm, TextInput, Select, CheckboxInput, DateTimeField, formset_factory, \
    inlineformset_factory, modelformset_factory, BaseInlineFormSet
from registration.models import Member, Membership, Joad_sessions, Pin_shoot, Joad_session_registration
from django import forms


logger = logging.getLogger(__name__)


class JoadSessionForm(ModelForm):
    class Meta:
        model = Joad_sessions
        fields = ['start_date', 'state']
        widgets = {'start_date': forms.TextInput(attrs={'placeholder': 'Start Date YYYY-MM-DD',
                                                        'class': 'form-control m-2 date_input'}), }
