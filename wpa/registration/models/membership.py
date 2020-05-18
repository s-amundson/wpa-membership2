from django.db import models
# from .member import Member


class Membership(models.Model):
    # fam_id = models.IntegerField()
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=3)
    post_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=150)
    levels = [('standard', 'Standard'),
              ('family', 'Family'),
              ('joad', 'JOAD'),
              ('senior', 'Senior')]
    level = models.CharField(max_length=20, choices=levels)
    reg_date = models.DateField()
    exp_date = models.DateField()
    # fam = models.IntegerField(null=True, default=None)
    benefactor = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    pay_code = models.CharField(max_length=50, null=True)
    # member = models.ForeignKey(Member, on_delete=models.CASCADE)
