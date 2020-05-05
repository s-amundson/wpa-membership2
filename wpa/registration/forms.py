from django.forms import ModelForm
from registration.models import Member, Family
from registration.widgets import BootstrapDateTimePickerInput
from django import forms
from tempus_dominus.widgets import DatePicker


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'street', 'city', 'state', 'post_code', 'phone', 'email', 'dob', 'level',
                  'benefactor']
        widgets = {'dob': DatePicker()}
        # dob =


class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ['fam_id', 'member']