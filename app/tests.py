from datetime import date

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from app.forms import RegistrationForm, ProfilePasswordChangeForm


class RegisterTestCase(TestCase):

    def test_register_username_correct(self):
        form_data = {
            'username': 'Jeyabal@-1',
            'password': '1234',
            'date_of_birth': '1989-03-10',
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_register_username_incorrect(self):
        form_data = {
            'username': 'Jeyabal#',
            'password': '1234',
            'date_of_birth': '1989-03-10',
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_register_password_incorrect(self):
        form_data = {
            'username': 'Jeyabal#',
            'password': '12345',
            'date_of_birth': '1989-03-10',
        }
        form = RegistrationForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_password_change_incorrect(self):
        form_data = {
            'old_password': '123',
            'new_password': 'jey123',
            'confirm_password': 'jey123',
        }
        form = ProfilePasswordChangeForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_password_change_correct(self):
        form_data = {
            'old_password': '1234',
            'new_password': '3456',
            'confirm_password': '3456',
        }
        form = ProfilePasswordChangeForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_register_sets_dob(self):
        client = Client()
        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1980-01-01',
        })
        self.assertRedirects(response, '/')
        user = User.objects.get(username='testing')
        self.assertEqual(user.profile.date_of_birth, date(1980, 1, 1))

    def test_user_profile_get_age_25(self):
        client = Client()
        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1980-01-01',
        })
        self.assertRedirects(response, '/')
        user = User.objects.get(username='testing')
        self.assertEqual(user.profile.get_age()['age_range'], '25+')

    def test_user_profile_get_age_20_24(self):
        client = Client()
        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '1995-01-01',
        })
        self.assertRedirects(response, '/')
        user = User.objects.get(username='testing')
        self.assertEqual(user.profile.get_age()['age_range'], '20-24')

    def test_user_profile_get_age_15_19(self):
        client = Client()
        response = client.post(reverse('user_register'), {
            'username': 'testing',
            'password': '1234',
            'date_of_birth': '2000-01-01',
        })
        self.assertRedirects(response, '/')
        user = User.objects.get(username='testing')
        self.assertEqual(user.profile.get_age()['age_range'], '15-19')
