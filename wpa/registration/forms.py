import logging

from django.db import OperationalError
from django.forms import ModelForm, TextInput, Select, CheckboxInput, DateTimeField, formset_factory, \
    inlineformset_factory, modelformset_factory, BaseInlineFormSet
from registration.models import Member, Membership, Joad_sessions, Pin_shoot, Joad_session_registration
from registration.widgets import FengyuanChenDatePickerInput
from django import forms
from tempus_dominus.widgets import DatePicker

logger = logging.getLogger(__name__)


def joad_sessions():
    sessions = Joad_sessions.objects.filter(state__exact='open')
    d = [("", "None")]
    try:  # this has caused a error when migration is needed, but also blocks migrations from working
        for s in sessions:
            d.append((str(s.start_date), str(s.start_date)))
    except OperationalError as e:  # pragma: no cover
        logging.error(f"Operational Error: {e}")
    logging.debug(f"session: {d}")
    return d


class CustomInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        # example custom validation across forms in the formset
        for form in self.forms:
            logging.debug(form)


class EmailValidate(ModelForm):
    class Meta:
        model = Membership
        fields = ['email', 'verification_code']
        widgets = {'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
                                             'class': "form-control m-2 email"}),
                   'verification_code': TextInput(attrs={'placeholder': 'Verification Code', 'autocomplete': 'off',
                                                  'class': "form-control m-2 not_empty"})}


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


class JoadSessionForm(ModelForm):
    class Meta:
        model = Joad_sessions
        fields = ['start_date', 'state']
        widgets = {'start_date': forms.TextInput(attrs={'placeholder': 'Start Date YYYY-MM-DD',
                                                        'class': 'form-control m-2 date_input'}), }


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

    # dob = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    # dob.widget_attrs({'placeholder': 'Date of Birth YYYY-MM-DD',
    #                   'class': 'form-control m-2 member-required dob', "form_id": "__prefix__"})

    def clean(self):
        logging.debug(self.data)
        super().clean()
        logging.debug(self.cleaned_data)
        j = self.cleaned_data.get('joad')
        logging.debug(j)
        # self.cleaned_data.update({'joad': (j, j)})

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'dob', 'joad']
        widgets = {'first_name': TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                  'class': "form-control m-2 member-required",
                                                  "form_id": "__prefix__"}),
                   'last_name': TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                 'class': "form-control m-2 member-required", "form_id": "__prefix__"}),
                   'dob': forms.TextInput(attrs={'placeholder': 'Date of Birth YYYY-MM-DD', "form_id": "__prefix__",
                                                 'class': 'form-control m-2 member-required dob',
                                                 'data-error-msg': "Please enter date in format YYYY-MM-DD"}),
                   }


MembershipFormSet = inlineformset_factory(Membership, Member, form=MemberForm, can_delete=True, extra=0, min_num=0,
                                          max_num=4)


# MembershipFormSet = ""


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
                   'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
                                             'class': "form-control m-2 email"}),
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
                   'shoot_date': TextInput(attrs={'append': 'fa fa-calendar', 'icon_toggle': True,
                                                  'class': "form-control date_input"}),
                   'distance': Select(attrs={'class': "form-control m-2"}, choices=((9, 9), (18, 18))),
                   'target': Select(attrs={'class': "form-control m-2"}, choices=((60, 60), (40, 40))),
                   'prev_stars': Select(attrs={'class': "form-control m-2"}),
                   'score': TextInput(attrs={'placeholder': 'Score', 'autocomplete': 'off',
                                             'class': "form-control m-2 numeric", 'required': ""})
                   }
#