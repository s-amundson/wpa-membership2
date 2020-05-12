from django.db import models
from .member import Member


class Family(models.Model):
    fam_id = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
