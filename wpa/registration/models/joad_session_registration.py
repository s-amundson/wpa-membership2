import uuid
from django.db import models
from django.utils.datetime_safe import date

from .member import Member
from .joad_sessions import Joad_sessions


class Joad_session_registration(models.Model):
    mem = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    pay_status = models.CharField(max_length=20)
    idempotency_key = models.UUIDField(default=str(uuid.uuid4()))
    session = models.ForeignKey(Joad_sessions, on_delete=models.DO_NOTHING)

    def joad_check_date(dob):
        d = date.today()
        # logging.debug(d.year)
        d = d.replace(year=d.year - 21)
        # logging.debug(dob)
        return dob > d