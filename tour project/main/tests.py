from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class StaticAssetTest(TestCase):
    def test_login_script_asset_exists(self):
        script_path = Path(settings.BASE_DIR) / 'main' / 'static' / 'js' / 'script.js'
        self.assertTrue(script_path.exists(), 'Expected script.js to exist for the login and welcome page interactions.')

    def test_login_page_has_create_account_link(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an account')

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')

    def test_register_view_creates_django_user(self):
        payload = {
            'full_name': 'New User',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPassword123',
        }

        response = self.client.post(reverse('register'), payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())

    def test_home_page_has_trip_planning_call_to_action(self):
        response = self.client.get(reverse('home_page_html'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Plan My Trip')

    def test_travel_plan_uses_working_tile_provider(self):
        response = self.client.get(reverse('travel_plan'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'basemaps.cartocdn.com')

    def test_travel_plan_page_loads(self):
        response = self.client.get(reverse('travel_plan'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Travel Plan')
        self.assertContains(response, 'Starting point')
        self.assertContains(response, 'End point')
        self.assertContains(response, 'Stop points')
        self.assertContains(response, 'Distance')
        self.assertContains(response, 'Day-wise itinerary')
