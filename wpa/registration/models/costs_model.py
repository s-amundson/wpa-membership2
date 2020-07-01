import logging
from django.db import models

logger = logging.getLogger(__name__)


class CostsModel(models.Model):
    name = models.CharField(max_length=40)
    membership = models.BooleanField(default=False)
    enabled = models.BooleanField(default=False)
