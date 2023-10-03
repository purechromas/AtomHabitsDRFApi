from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from users.models import User


class BaseApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email='test@gmail.com')
        self.user.set_password('test')
        self.user.is_verified = True
        self.user.save()

        url_login = reverse('users:token_obtain_pair')
        data = {'email': 'test@gmail.com', 'password': 'test'}
        resp = self.client.post(url_login, data)
        token = resp.json()['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
