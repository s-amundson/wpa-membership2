import logging
from django.db import models
from .membership import Membership

logger = logging.getLogger(__name__)


class Member(models.Model):
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()


    # def check_duplicate(self, form_data):
    #     # check for duplicate
    #     try:
    #         reg_mem = Member.objects.filter(first_name=form_data['first_name'],
    #                                         last_name=form_data['last_name'])
    #     except Member.DoesNotExist:  # pragma: no cover
    #         reg_mem = None
    #     if reg_mem is not None and len(reg_mem) > 0:
    #         logging.debug(f"Duplicate(s) may exist {reg_mem}, len={len(reg_mem)}")
    #         col = ["street", "city", "state", "zip", "phone", "email", "dob"]
    #         for row in reg_mem:
    #
    #             matches = 0
    #             if row.street == form_data['street']:
    #                 matches += 1
    #             if row.city == form_data['city']:
    #                 matches += 1
    #             if row.state == form_data['state']:
    #                 matches += 1
    #             if row.post_code == form_data['post_code']:
    #                 matches += 1
    #             if row.phone == form_data['phone']:
    #                 matches += 1
    #             if row.email == form_data['email']:
    #                 matches += 1
    #             if row.dob == form_data['dob']:
    #                 matches += 1
    #
    #             if matches >= len(col) - 2:
    #                 logging.debug('Found Match')
    #                 return True
    #     return False
