import logging

from django.forms import ModelForm, TextInput
from registration.models import Membership

logger = logging.getLogger(__name__)


class EmailValidate(ModelForm):
    class Meta:
        model = Membership
        fields = ['email', 'verification_code']
        widgets = {'email': TextInput(attrs={'placeholder': 'Email', 'autocomplete': 'off', 'name': 'email',
                                             'class': "form-control m-2 email"}),
                   'verification_code': TextInput(attrs={'placeholder': 'Verification Code', 'autocomplete': 'off',
                                                  'class': "form-control m-2 not_empty"})}
