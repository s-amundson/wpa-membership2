import logging

from django import forms
from django.forms import ModelForm, TextInput, Select, CheckboxInput
from registration.models import Member
from . import joad_sessions

logger = logging.getLogger(__name__)


class SelectChoiceField(forms.ChoiceField):
    def clean(self, value):
        logging.debug(value)
        # super().clean(value)
        return value


class MemberForm(ModelForm):
    # def __init__(self, values, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    joad = SelectChoiceField(choices=joad_sessions(), widget=Select(attrs={'class': "form-control m-2 costs"}))
    joad.required = False
    DELETE = forms.BooleanField(widget=CheckboxInput(attrs={'class': "form-control m-2 custom-control-input"}),
                               )


    def clean(self):
        logging.debug(self.data)
        super().clean()
        logging.debug(self.cleaned_data)
        j = self.cleaned_data.get('joad')
        logging.debug(j)
        # self.cleaned_data.update({'joad': (j, j)})

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'dob', 'joad', 'DELETE']
        widgets = {'first_name': TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                  'class': "form-control m-2 member-required",
                                                  "form_id": "__prefix__"}),
                   'last_name': TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                 'class': "form-control m-2 member-required", "form_id": "__prefix__"}),
                   'dob': forms.TextInput(attrs={'placeholder': 'Date of Birth YYYY-MM-DD', "form_id": "__prefix__",
                                                 'class': 'form-control m-2 member-required dob',
                                                 'data-error-msg': "Please enter date in format YYYY-MM-DD"}),
                   }

