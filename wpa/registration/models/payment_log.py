from django.db import models


class Payment_log(models.Model):
    members = models.CharField(max_length=50, null=True)
    reg_date = models.DateField()
    checkout_created_time = models.DateTimeField()
    checkout_id = models.CharField(max_length=50, null=True)
    order_id = models.CharField(max_length=50, null=True)
    location_id = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=20, null=True)
    total_money = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=50, null=True)
    idempotency_key = models.UUIDField()
    receipt = models.CharField(max_length=100, null=True)
