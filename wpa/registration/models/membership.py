import logging
from django.conf import settings
from django.db import models

from registration.src.square_helper import line_item

logger = logging.getLogger(__name__)


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
    # member = models.ForeignKey('registration.Member', on_delete=models.CASCADE)

    @staticmethod
    def line_items_from_membership(membership):
        from . import Joad_session_registration
        benefactor = False

        ik = membership.verification_code
        if membership.benefactor:
            benefactor = True
        if benefactor:
            cost = settings.COSTS['benefactor']
            lines = [line_item("Benefactor Membership", 1, cost)]
        else:
            cost = settings.COSTS[f"{membership.level}_membership"]
            lines = [line_item("Membership", 1, cost)]

        js = Joad_session_registration.objects.filter(idempotency_key=ik, pay_status='new')
        if len(js) > 0:
            logging.debug(js[0].session)
            cost = settings.COSTS['joad_session']
            lines.append(line_item(f'Joad Session {js[0].session.start_date.isoformat()}', len(js), cost))
            logging.debug(lines)
        return {'line_items': lines, 'idempotency_key':ik}
