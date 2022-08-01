from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import User


def mock_post(code, json, *args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data

        def json(self):
            return self._json

        def __iter__(self):
            return []

        @property
        def text(self):
            return str(self._json)

    return MockResponse(code, json)


def mock_get(code, json, *args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json = json_data

        def json(self):
            return self._json

        def __iter__(self):
            return []

        @property
        def text(self):
            return str(self._json)

    return MockResponse(code, json)


class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='a@yoo.com', first_name='a', last_name='a', is_created_in_keycloak=False, role='admin')

        self.user_password = '1234'
        self.user_data = {
            'username': self.user.username,
            'email': self.user.username,
            'enabled': True,
            'emailVerified': True,
            'firstName': self.user.first_name,
            'lastName': self.user.last_name,
            'requiredActions': [],
            'attributes': {'role': 'admin'},
            'credentials': [
                {
                    'type': 'password',
                    'value': self.user_password,
                    'temporary': False
                }
            ]
        }

        self.user.set_password(self.user_password)
        self.user.save()

        self.get_token_url = reverse('token_obtain_pair')

    def test_login_local_user_not_on_keycloak(self):
        """
            user not presented on
        """
        data = {
            'username': self.user.username,
            'password': self.user_password,
        }
        response = self.client.post(self.get_token_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    @patch('requests.post', side_effect=[mock_post(200, {'access_token': '0000', 'refresh_token': '1111'})])
    def test_login_local_user_on_keycloak(self, _):
        """
            mock get token to let it back token and refresh token
        """
        data = {
            'username': self.user.username,
            'password': self.user_password,
        }
        response = self.client.post(self.get_token_url, data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'access_token': '0000',
                'refresh_token': '1111'
            }
        )


class AdminTestCase(TestCase):
    def setUp(self):
        self.admin_url = reverse('admin')
        self.normal_url = reverse('normal')
        self.admin_user = User.objects.create(
            username='aboda', first_name='a', last_name='a', is_created_in_keycloak=False, role='admin')
        self.admin_user = User.objects.create(
            username='ahmed', first_name='a', last_name='a', is_created_in_keycloak=False, role='normal')

    def test_admin_not_authenticated(self):
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 401)

    @patch('requests.post',
           side_effect=[mock_post(200, {'preferred_username': 'aboda', 'given_name': 'abdullah', 'family_name': 'elkasass'})])
    def test_admin_authenticated_token_empty(self, _):
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 401)

    @patch('requests.post',
            side_effect=[
            mock_post(200, {'preferred_username': 'aboda', 'given_name': 'abdullah', 'family_name': 'elkasass'}),
            mock_post(200, {'access_token': '0000', 'refresh_token': '1111'})
            ]
        )
    @patch(
        'requests.get',
        side_effect=[mock_get(200, [
                {'attributes': {'role': ['admin']}}
            ])
        ]
    )
    def test_admin_page_using_admin_user(self, *args):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer 0000'
        }
        response = self.client.get(self.admin_url, HTTP_AUTHORIZATION='Bearer 0000', headers=headers)
        self.assertEqual(response.status_code, 200)

    @patch(
        'requests.post',
        side_effect=[mock_post(200, {
                'preferred_username': 'ahmed',
                'given_name': 'abdullah',
                'family_name': 'elkasass'}),
                mock_post(200, {
            'access_token': '0000',
            'refresh_token': '1111'})
        ]
    )
    @patch(
        'requests.get',
        side_effect=[mock_get(200, [
                {'attributes': {'role': ['normal']}}
            ])
        ]
    )
    def test_admin_page_using_normal_user(self, *args):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer 0000'
        }
        response = self.client.get(self.admin_url, HTTP_AUTHORIZATION='Bearer 0000', headers=headers)
        self.assertEqual(response.status_code, 403)

    @patch(
        'requests.post',
        side_effect=[mock_post(200, {
                'preferred_username': 'ahmed',
                'given_name': 'abdullah',
                'family_name': 'elkasass'}),
                mock_post(200, {
            'access_token': '0000',
            'refresh_token': '1111'})
        ]
    )
    @patch(
        'requests.get',
        side_effect=[mock_get(200, [
                {'attributes': {'role': ['normal']}}
            ])
        ]
    )
    def test_normal_page_using_normal_user(self, *args):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer 0000'
        }
        response = self.client.get(self.normal_url, HTTP_AUTHORIZATION='Bearer 0000', headers=headers)
        self.assertEqual(response.status_code, 200)

    @patch('requests.post', side_effect=[
            mock_post(200, {'preferred_username': 'ahmed', 'given_name': 'abdullah', 'family_name': 'elkasass'}),
            mock_post(200, {'access_token': '0000', 'refresh_token': '1111'})])
    @patch(
        'requests.get',
        side_effect=[mock_get(200, [
                {'attributes': {'role': ['admin']}}
            ])
        ]
    )
    def test_normal_page_using_admin_user(self, *args):
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer 0000'
        }
        response = self.client.get(self.normal_url, HTTP_AUTHORIZATION='Bearer 0000', headers=headers)
        self.assertEqual(response.status_code, 403)


class TestUserManager(TestCase):
    def test_manager_create_super_user(self):
        user = User.objects.create_superuser(
            username='admin@ua.com', password='123', first_name='a', last_name='a', is_created_in_keycloak=False, role='admin'
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertTrue(User.objects.filter(id=user.id).exists())

    def test_manager_create_user_success(self):
        user = User.objects.create(
            username='admin@ua.com', password='123', first_name='a', last_name='a', is_created_in_keycloak=False, role='admin'
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertTrue(User.objects.filter(id=user.id).exists())

    def test_manager_missing_email(self):
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                password='123', first_name='a', last_name='a', is_created_in_keycloak=False, role='admin')
