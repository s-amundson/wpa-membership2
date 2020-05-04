from django.db import models


# Create your models here.
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
    level = models.CharField(max_length=20)
    reg_date = models.DateField()
    exp_date = models.DateField()
    fam = models.IntegerField(null=True, default=None)
    benefactor = models.BooleanField(default=False)
    email_code = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    pay_code = models.CharField(max_length=50, null=True)


class Family(models.Model):
    fam_id = models.IntegerField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)


class Joad_sessions(models.Model):
    start_date = models.DateField()
    c = [('scheduled', 'scheduled'), ('open', 'open'), ('closed', 'closed')]
    state = models.CharField(max_length=20, null=True, choices=c)

    def __str__(self):
        return f"start date: {self.start_date}, state: {self.state}"


class Joad_session_registration(models.Model):
    mem = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    pay_status = models.CharField(max_length=20)
    email_code = models.CharField(max_length=50, null=True, default=None)
    session = models.ForeignKey(Joad_sessions, on_delete=models.DO_NOTHING)


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


class Pin_shoot(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    club = models.CharField(max_length=45)
    category = models.CharField(max_length=20)
    bow = models.CharField(max_length=45)
    shoot_date = models.DateField()
    distance = models.IntegerField()
    target = models.IntegerField()
    prev_stars = models.IntegerField()
    stars = models.IntegerField()
    wpa_membership_number = models.IntegerField()
    score = models.IntegerField()


class Renewal_email_log:
    mem = models.ForeignKey(Member, on_delete=models.DO_NOTHING)
    sent_timestamp = models.DateField()
