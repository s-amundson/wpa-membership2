import uuid
from django.db import models
from .member import Member
from .joad_sessions import Joad_sessions


class Joad_session_registration(models.Model):
    mem = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    pay_status = models.CharField(max_length=20)
    idempotency_key = models.UUIDField(default=str(uuid.uuid4()))
    session = models.ForeignKey(Joad_sessions, on_delete=models.DO_NOTHING)
