import logging
from django.db import models

logger = logging.getLogger(__name__)


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

    def check_duplicate(self, form_data):
        # check for duplicate
        try:
            reg_mem = Member.objects.filter(first_name=form_data['first_name'],
                                            last_name=form_data['last_name'])
        except Member.DoesNotExist:
            reg_mem = None
        if reg_mem is not None and len(reg_mem) > 0:
            logging.debug(f"Duplicate(s) may exist {reg_mem}, len={len(reg_mem)}")
            col = ["street", "city", "state", "zip", "phone", "email", "dob"]
            for row in reg_mem:

                matches = 0
                if row.street == form_data['street']:
                    matches += 1
                if row.city == form_data['city']:
                    matches += 1
                if row.state == form_data['state']:
                    matches += 1
                if row.post_code == form_data['post_code']:
                    matches += 1
                if row.phone == form_data['phone']:
                    matches += 1
                if row.email == form_data['email']:
                    matches += 1
                if row.dob == form_data['dob']:
                    matches += 1

                if matches >= len(col) - 2:
                    logging.debug('Found Match')
                    return True
        return False
