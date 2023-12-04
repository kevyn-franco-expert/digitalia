from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser as User


class RegisterPageViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register/index.html')


class DashBoardViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_redirect_if_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('room'))

    def test_stay_on_page_if_not_authenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class MessageViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room_name = 'test_room'

    def test_load_page_if_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('message-room', kwargs={'room_name': self.room_name}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'message/index.html')
