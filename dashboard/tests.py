from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from users.models.user import User
from teams.models import Team
from activities.models.activity_type import ActivityType
from activities.models.activity import Activity


class DashboardExportInjectionTests(TestCase):
    def setUp(self):
        team = Team.objects.create(name='Team A')
        self.admin = User.objects.create_user(
            email='admin@example.com', password='pass', name='Admin', rol=User.ADMIN
        )
        u = User.objects.create_user(
            email='user@example.com', password='pass', name='User One', team=team
        )
        t = ActivityType.objects.create(name='Commit válido', points=4)
        Activity.objects.create(activity_type=t, user=u, date=timezone.now().date())
        self.client.force_login(self.admin)

    def test_export_ranking_excel_safe(self):
        url = reverse('dashboard:export_ranking_excel')
        resp = self.client.get(url, {'period': "diario; DROP TABLE x;--"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', resp['Content-Type'])

    def test_export_ranking_pdf_safe(self):
        url = reverse('dashboard:export_ranking_pdf')
        resp = self.client.get(url, {'period': "' OR '1'='1"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/pdf', resp['Content-Type'])