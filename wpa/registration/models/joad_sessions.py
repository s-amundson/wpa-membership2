from django.db import models


class Joad_sessions(models.Model):
    start_date = models.DateField()
    c = [('scheduled', 'scheduled'), ('open', 'open'), ('closed', 'closed')]
    state = models.CharField(max_length=20, null=True, choices=c)

    def __str__(self):
        return f"start date: {self.start_date}, state: {self.state}"
