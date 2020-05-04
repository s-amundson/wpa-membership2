from django.forms import ModelForm
from .models import Member

class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'street', 'city', 'state', 'post_code', 'phone', 'email', 'dob', 'level',
                  'benefactor']

        #     first_name = models.CharField(max_length=100)
        #     last_name = models.CharField(max_length=100)
        #     street = models.CharField(max_length=150)
        #     city = models.CharField(max_length=150)
        #     state = models.CharField(max_length=3)
        #     post_code = models.CharField(max_length=10)
        #     phone = models.CharField(max_length=20)
        #     email = models.EmailField(max_length=150)
        #     dob = models.DateField()
        #     level = models.CharField(max_length=20)
        #     reg_date = models.DateField()
        #     exp_date = models.DateField()
        #     fam = models.IntegerField(null=True, default=None)
        #     benefactor = models.BooleanField(default=False)
        #     email_code = models.CharField(max_length=50, null=True)
        #     status = models.CharField(max_length=50, null=True)
        #     pay_code = models.CharField(max_length=50, null=True)