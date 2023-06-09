from django.contrib.auth import get_user
from .models import CustomUser
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class RegisterTestCase(TestCase):
    def test_unique_username(self):
        user=CustomUser.objects.create(
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
                'username': 'oybek',
                'first_name': 'Oybeke',
                'last_name': 'Saydullayeve',
                'email': 'oybekjohn01@gmeail.com',
                'password': 'oybek01e21',
            }
        )
        user_count = CustomUser.objects.count()
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
        count = CustomUser.objects.count()
        self.assertEqual(count, 0)

    def test_valid_username(self):
        self.client.post(
            reverse('register'),
            data={
                'first_name': 'Oybek',
                'last_name': 'Saydullayev',
                'email': 'oybekjohn01@gmail.com',
                'password': 'oybek0121'
            }
        )
        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 0)


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='saydullayev',
            email='oybek@gmail.com'
        )
        self.db_user.set_password('password')
        self.db_user.save()

    def test_success_login(self):
        self.client.post(
            reverse('login'),
            data={
                'username': 'oybek',
                'password': 'password'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_success_logout(self):
        self.client.login(username='oybek', password='password')

        self.client.get(reverse('logout'))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('login'),
            data={
                'username': 'oybek',
                'password': 'wrong-password'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


        self.client.post(
            reverse('login'),
            data={
                'username': 'wrong-username',
                'password': 'password'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + '?next=/users/profile/')

    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='Saydullayev',
            email='oybekjonh01@gmail.com',
        )
        user.set_password('password')
        user.save()

        self.client.login(username='oybek', password='password')

        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)

    def test_profile_update(self):
        user = CustomUser.objects.create(
            username='oybek',
            first_name='Oybek',
            last_name='Saydullayev',
            email='oybekjohn01@gmail.com',
        )
        user.set_password('password')
        user.save()

        self.client.login(username='oybek', password='password')

        response = self.client.post(
            reverse('profile-edit'),
            data={
                'username': 'oybekjohn',
                'first_name': 'Oybek',
                'last_name': 'Saydullayev',
                'email': 'oybekjohn02@gmail.com',
            }
        )

        user = CustomUser.objects.get(pk=user.pk)

        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'oybekjohn')
        self.assertEqual(user.email, 'oybekjohn02@gmail.com')
        self.assertEqual(response.url, reverse('profile'))
