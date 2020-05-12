import logging

from django.forms import ModelForm, TextInput, Select, CheckboxInput, DateTimeField
from registration.models import Member, Family, Joad_sessions, Pin_shoot, Joad_session_registration
from registration.widgets import BootstrapDateTimePickerInput
from django import forms
from tempus_dominus.widgets import DatePicker

logger = logging.getLogger(__name__)

def joad_sessions():
    sessions = Joad_sessions.objects.filter(state__exact='open')
    d = [("", "None")]
    for s in sessions:
        d.append((str(s.start_date), str(s.start_date)))
    return d


class EmailValidate(ModelForm):
    verification_code = forms.CharField(required=True, widget=TextInput(
        attrs={'placeholder': 'Verification Code', 'autocomplete': 'off',
               'class': "form-control m-2 not_empty"}))
    class Meta:
        model = Member
        fields = ['email', 'verification_code']
        widgets = {'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
                                             'class': "form-control m-2 email"})}


class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ['fam_id', 'member']


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


class MemberForm(ModelForm):
    # def __init__(self, values, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    terms = forms.BooleanField(widget=CheckboxInput(attrs={'class': "form-control m-2 custom-control-input"}),
                               required=True)

    joad = forms.ChoiceField(choices=joad_sessions(), widget=Select(attrs={'class': "form-control m-2 costs"}))
    joad.required = False

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
                   'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
                                             'class': "form-control m-2 email"}),
                   'dob': DatePicker(attrs={'append': 'fa fa-calendar', 'icon_toggle': True,
                                            'class': "form-control"}),
                   'level': Select(attrs={'class': "form-control m-2 costs "}),
                   'benefactor': CheckboxInput(attrs={'class': "form-control m-2 custom-control-input costs"})
                   }



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
                   'shoot_date': DatePicker(attrs={'append': 'fa fa-calendar', 'icon_toggle': True,
                                                   'class': "form-control"}),
                   'distance': Select(attrs={'class': "form-control m-2"}),
                   'target': Select(attrs={'class': "form-control m-2"}),
                   'prev_stars': Select(attrs={'class': "form-control m-2"}),
                   'score': TextInput(attrs={'placeholder': 'Score', 'autocomplete': 'off',
                                             'class': "form-control m-2 numeric"})
                   }
