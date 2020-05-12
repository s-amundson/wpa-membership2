from django.db import models


# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=3)
    post_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=150)
    dob = models.DateField()
    levels = [  # ('invalid', 'Membership Level'),
              ('standard', 'Standard'),
              ('family', 'Family'),
              ('joad', 'JOAD'),
              ('senior', 'Senior')]
    level = models.CharField(max_length=20, choices=levels)
    reg_date = models.DateField()
    exp_date = models.DateField()
    fam = models.IntegerField(null=True, default=None)
    benefactor = models.BooleanField(default=False)
    email_code = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    pay_code = models.CharField(max_length=50, null=True)
