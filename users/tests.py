from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class RegisterTestCase(TestCase):
    def test_unique_username(self):
        user=User.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='Saydullayev',
        )
        user.set_password(
            'anypassword'
        )
        user.save()

        response2 = self.client.post(
            reverse('register'),
            data={
                'username':'oybek',
                'first_name':'Oybeke',
                'last_name': 'Saydullayeve',
                'email': 'oybekjohn01@gmeail.com',
                'password': 'oybek01e21',
            }
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

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

    def test_valid_username(self):
        self.client.post(
            reverse('register'),
            data={
                'first_name': 'Oybek',
                'last_name': 'Saydullayev',
                'email': 'oybekjohn01gmail.com',
                'password': 'oybek0121'
            }
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 0)