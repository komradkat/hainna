from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from fleet.models import Terminal

class CoreEfficiencyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='password', role='Administrator')
        self.client.login(username='testuser', password='password')
        Terminal.objects.create(name="Test Terminal", is_master_hub=True)

    def test_health_check(self):
        from unittest.mock import patch
        with patch('fleet.traccar.is_connected', return_value=True):
            response = self.client.get(reverse('health_check'))
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'healthy')
            self.assertEqual(data['database'], 'online')
            self.assertEqual(data['traccar'], 'online')

    def test_dashboard_load(self):
        # First load - populates cache
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Second load - should be served from cache
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
