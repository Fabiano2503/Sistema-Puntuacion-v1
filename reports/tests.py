from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from users.models.user import User
from teams.models import Team
from activities.models.activity_type import ActivityType
from activities.models.activity import Activity


class SqlInjectionSafetyTests(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team A')
        self.admin = User.objects.create_user(
            email='admin@example.com', password='pass', name='Admin', rol=User.ADMIN
        )
        self.user = User.objects.create_user(
            email='user@example.com', password='pass', name='User One', team=self.team
        )
        t = ActivityType.objects.create(name='Commit válido', points=4)
        Activity.objects.create(activity_type=t, user=self.user, date=timezone.now().date())

        self.client.force_login(self.admin)

    def test_history_rejects_sql_injection_user_param(self):
        url = reverse('reports:reports_history')
        payloads = [
            "1 OR 1=1",
            "1; DROP TABLE users_user;--",
            "' OR '1'='1",
            "1 union select null",
        ]
        for inj in payloads:
            resp = self.client.get(url, {'user': inj})
            self.assertEqual(resp.status_code, 200)
            # Should not error and should render template
            self.assertIn('text/html', resp['Content-Type'])

    def test_history_rejects_sql_injection_team_param(self):
        url = reverse('reports:reports_history')
        resp = self.client.get(url, {'team': "0; DROP TABLE teams_team;--"})
        self.assertEqual(resp.status_code, 200)

    def test_history_ignores_invalid_dates(self):
        url = reverse('reports:reports_history')
        resp = self.client.get(url, {'start': '2025-13-40', 'end': '2025-13-41'})
        self.assertEqual(resp.status_code, 200)

    def test_export_history_excel_safe(self):
        url = reverse('reports:export_history_excel')
        resp = self.client.get(url, {
            'period': 'biweekly',
            'user': "' OR '1'='1",
            'team': '1 OR 1=1'
        })
        self.assertEqual(resp.status_code, 200)
        ct = resp['Content-Type']
        self.assertTrue(
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in ct or 'text/csv' in ct,
            msg=f'Unexpected content type for export: {ct}'
        )

    def test_export_history_pdf_safe(self):
        url = reverse('reports:export_history_pdf')
        resp = self.client.get(url, {
            'period': 'biweekly',
            'start': '2025-01-01',
            'end': '2025-01-31',
            'user': '0; drop table x;--'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/pdf', resp['Content-Type'])

# Create your tests here.
