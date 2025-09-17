from django.db import models

class Period(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    BIWEEKLY = 'biweekly'
    PERIOD_CHOICES = [
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (BIWEEKLY, 'Biweekly'),
    ]

    type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    startDate = models.DateField()
    endDate = models.DateField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type.capitalize()} - {self.startDate} to {self.endDate}'