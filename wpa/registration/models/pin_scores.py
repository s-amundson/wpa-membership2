from django.db import models


class Pin_scores(models.Model):
    c = [('barebow', 'Barebow/Basic Compound/Traditional'), ('olympic', 'Olympic Recurve'), ('compound', 'Compound')]
    bow = models.CharField(max_length=45, choices=c)
    category = models.CharField(max_length=20, choices=[('joad_indoor', 'JOAD Indoor')])
    distance = models.IntegerField(choices=[(9, 9), (18, 18)])
    target = models.IntegerField(choices=[(40, 40), (60, 60), (80, 80), (122, 122)])
    score = models.IntegerField()
    stars = models.IntegerField()
