import logging

from django.forms import ModelForm, TextInput, Select, CheckboxInput, DateTimeField
from registration.models import Member, Family, Joad_sessions
from registration.widgets import BootstrapDateTimePickerInput
from django import forms
from tempus_dominus.widgets import DatePicker

logger = logging.getLogger(__name__)


class MemberForm(ModelForm):
    # def __init__(self, values, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    terms = forms.BooleanField()
    terms.required = True

    sessions = Joad_sessions.objects.filter(state__exact='open')
    d = []
    for s in sessions:
        logging.debug(s)
        d.append((str(s.start_date), str(s.start_date)))
    logging.debug(d)
    joad = forms.ChoiceField(choices=d)
    joad.required = False
    # joad.choices = d

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'street', 'city', 'state', 'post_code', 'phone', 'email', 'dob', 'level',
                  'joad', 'benefactor', 'terms']
        widgets = {'first_name': TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                  'class': "form-control m-2 not_empty"}),
                   'last_name': TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                 'class': "form-control m-2 not_empty"}),
                   'street': TextInput(attrs={'placeholder': 'Street', 'autocomplete': 'off',
                                              'class': "form-control m-2 not_empty"}),
                   'city': TextInput(attrs={'placeholder': 'City', 'autocomplete': 'off',
                                            'class': "form-control m-2 not_empty"}),
                   'state': TextInput(attrs={'placeholder': 'State', 'autocomplete': 'off',
                                             'class': "form-control m-2 not_empty"}),
                   'post_code': TextInput(attrs={'placeholder': 'Zip', 'autocomplete': 'off',
                                                 'class': "form-control m-2 not_empty"}),
                   'phone': TextInput(attrs={'placeholder': 'Phone', 'autocomplete': 'off',
                                             'class': "form-control m-2"}),
                   'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name':'email',
                                             'class': "form-control m-2 email"}),
                   'dob': DatePicker(attrs={'append': 'fa fa-calendar', 'icon_toggle': True}),
                   'level': Select(attrs={'class': "m-2"}),
                   'joad': Select(attrs={'class': "form-control m-2"}),
                   'benefactor': CheckboxInput(attrs={'class': "form-control m-2 custom-control-input"}),
                   'terms': CheckboxInput(attrs={'class': "form-control m-2 custom-control-input"})
                   }
        # dob = DateTimeField(
        #         input_formats=['%d/%m/%Y %H:%M'],
        #         widget=forms.DateTimeInput(attrs={
        #             'class': 'form-control datetimepicker-input',
        #             'data-target': '#datetimepicker1'
        #         })
        #     )


class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ['fam_id', 'member']
