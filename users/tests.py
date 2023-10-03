from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class TestUserRegistrationCreateAPIView(APITestCase):
    def setUp(self) -> None:
        self.registration_url = reverse('users:registration')
        self.user_diff_pass = {"email": "test@gmail.com", "password": "qwe123", "password1": "qwe124"}
        self.user_correct_data = {"email": "test@gmail.com", "password": "123qwe", "password1": "123qwe"}

    def test_password_not_match(self):
        response = self.client.post(self.registration_url, self.user_diff_pass)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'password1': ['Passwords do not match']})

    def test_email_already_exists(self):
        _ = self.client.post(self.registration_url, self.user_correct_data)
        response = self.client.post(self.registration_url, self.user_correct_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {'email': ['user with this Email address already exists.']}
        )

    def test_user_was_created(self):
        response = self.client.post(self.registration_url, self.user_correct_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {'message': 'Registration was successful. Check your email for verification.'}
        )


class TestUserEmailVerificationAPIView(APITestCase):
    def setUp(self) -> None:
        self.registration_url = reverse('users:registration')
        self.verification_url = reverse('users:verification')
        self.user_create = {"email": "test@gmail.com", "password": "123qwe", "password1": "123qwe"}
        self.client.post(self.registration_url, self.user_create)

    def test_verification_success(self):
        user_before_verification = User.objects.get(email='test@gmail.com')
        verification_number = user_before_verification.verification_number
        self.assertIsInstance(verification_number, int)
        self.assertEqual(user_before_verification.is_verified, False)

        url = self.verification_url + f'?verification_number={verification_number}'
        response = self.client.get(url)

        user_after_verification = User.objects.get(email='test@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': 'You were verified successfully.'})
        self.assertEqual(user_after_verification.is_verified, True)
        self.assertIsNone(user_after_verification.verification_number, None)


class TestCustomTokenObtainPairView(APITestCase):
    def setUp(self) -> None:
        reg_url = reverse('users:registration')
        reg_data = {"email": "test@gmail.com", "password": "123qwe", "password1": "123qwe"}
        self.client.post(reg_url, reg_data)

        self.token_url = reverse('users:token_obtain_pair')
        self.login_data = {"email": "test@gmail.com", "password": "123qwe"}

    def test_token_obtain_without_verification(self):
        response = self.client.post(self.token_url, self.login_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(), {'detail': 'Your email is not verified, check your email.'}
        )

    def test_token_obtain_with_verification(self):
        user = User.objects.get(email='test@gmail.com')
        ver_url = reverse('users:verification') + f'?verification_number={user.verification_number}'

        self.client.get(ver_url)

        response = self.client.post(self.token_url, self.login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), dict)
        self.assertEquals(len(response.json().keys()), 2)
