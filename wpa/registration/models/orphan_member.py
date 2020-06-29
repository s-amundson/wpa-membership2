import logging
from django.db import models
from .membership import Membership

logger = logging.getLogger(__name__)


class OrphanMember(models.Model):
    member_id = models.IntegerField()
    membership = models.IntegerField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    orphan_date = models.DateField()
