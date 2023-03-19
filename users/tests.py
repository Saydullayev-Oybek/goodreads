from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class RegisterTestCase(TestCase):
    def test_unique_username(self):
        response1 = self.client.post(
            reverse('register'),
            data = {
                'username':'oybek',
                'first_name':'Oybek',
                'last_name': 'Saydullayev',
                'email': 'oybekjohn01@gmail.com',
                'password': 'oybek0121'
            }
        )
        response2 = self.client.post(
            reverse('register'),
            data = {
                'username':'oybek',
                'first_name':'Oybeke',
                'last_name': 'Saydullayeve',
                'email': 'oybekjohn01@gmeail.com',
                'password': 'oybek01e21'
            }
        )

        self.assertFormError(response2, 'user_form', 'username', 'A user with that username already exists.')

    def test_valid_email(self):
        response = self.client.post(
            reverse('register'),
            data={
            'username':'oybek',
            'first_name':'Oybek',
            'last_name': 'Saydullayev',
            'email': 'oybekjohn01gmail.com',
            'password': 'oybek0121'
               }
        )
        count = User.objects.count()
        self.assertEqual(count, 0)