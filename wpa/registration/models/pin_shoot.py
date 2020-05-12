from django.db import models


class Pin_shoot(models.Model):
    star_choices = []
    for i in range(12):
        star_choices.append((i,i))
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    club = models.CharField(max_length=45, null=True)
    category = models.CharField(max_length=20, choices=[('joad_indoor', 'JOAD Indoor')])
    c = [('barebow', 'Barebow/Basic Compound/Traditional'), ('olympic', 'Olympic Recurve'), ('compound', 'Compound')]
    bow = models.CharField(max_length=45, choices=c)
    shoot_date = models.DateField()
    distance = models.IntegerField()
    target = models.IntegerField(choices=[(40, 40), (60, 60), (80, 80), (122, 122)])
    prev_stars = models.IntegerField(choices=star_choices)
    stars = models.IntegerField()
    wpa_membership_number = models.IntegerField(null=True)
    score = models.IntegerField()
