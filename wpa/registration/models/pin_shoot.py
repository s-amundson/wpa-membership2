from django.db import models
from .pin_scores import Pin_scores


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

    def calculate_pins(self):
        """Calculates the pins based off of target size, distance, bow class and score"""
        self.stars = 0
        rows = Pin_scores.objects.filter(category=self.category,
                                         bow=self.bow,
                                         distance=self.distance,
                                         target=self.target,
                                         score__lte=self.score)

        for row in rows:
            if row.stars > self.stars:
                self.stars = row.stars
        return self.stars

    def save(self, *args, **kwargs):
        if self.stars is None:
            self.calculate_pins()
        super().save(*args, **kwargs)  # Call the "real" save() method.