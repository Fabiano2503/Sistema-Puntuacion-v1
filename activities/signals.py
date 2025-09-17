from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models.activity import Activity
from teams.models import Team
from django.db.models import Sum

def update_team_points(team):
    if not team:
        return
    total = Activity.objects.filter(user__team=team).aggregate(
        total=Sum('activity_type__points')
    )['total'] or 0
    team.total_points = total
    team.save(update_fields=['total_points'])

@receiver(post_save, sender=Activity)
def activity_saved(sender, instance, **kwargs):
    update_team_points(instance.user.team)

@receiver(post_delete, sender=Activity)
def activity_deleted(sender, instance, **kwargs):
    update_team_points(instance.user.team)