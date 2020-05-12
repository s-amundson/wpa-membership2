from django.db import models
from .member import Member


class Renewal_email_log:
    mem = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    sent_timestamp = models.DateField()
