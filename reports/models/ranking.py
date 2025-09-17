from django.db import models
from .period import Period
from users.models.user import User

class Ranking(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    position = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)

    class Meta:
        unique_together = ('period', 'user')

    def __str__(self):
        return f'{self.user.name} - Posición {self.position} en {self.period}'