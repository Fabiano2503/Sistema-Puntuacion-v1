from django.db import models
from users.models.user import User
from .activity_type import ActivityType

class Activity(models.Model):
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    evidence = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.activity_type.name} by {self.user.name}'