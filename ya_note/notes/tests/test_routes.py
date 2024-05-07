from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )

    def test_pages_availability(self):
        users_urls_statuses = (
            (self.client, ('notes:home', None), HTTPStatus.OK),
            (self.client, ('users:login', None), HTTPStatus.OK),
            (self.client, ('users:logout', None), HTTPStatus.OK),
            (self.client, ('users:signup', None), HTTPStatus.OK),
            (self.author, ('notes:list', None), HTTPStatus.OK),
            (self.author, ('notes:add', None), HTTPStatus.OK),
            (self.author, ('notes:success', None), HTTPStatus.OK),
            (self.author, ('notes:detail', (self.note.slug,)), HTTPStatus.OK),
            (self.author, ('notes:edit', (self.note.slug,)), HTTPStatus.OK),
            (self.author, ('notes:delete', (self.note.slug,)), HTTPStatus.OK),
            (self.reader, ('notes:detail', (self.note.slug,)),
             HTTPStatus.NOT_FOUND),
            (self.reader, ('notes:edit', (self.note.slug,)),
             HTTPStatus.NOT_FOUND),
            (self.reader, ('notes:delete', (self.note.slug,)),
             HTTPStatus.NOT_FOUND),
        )
        for user, urls, status in users_urls_statuses:
            name, args = urls
            if user != self.client:
                self.client.force_login(user)
            with self.subTest(user=user, name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirects(self):
        login_url = reverse('users:login')
        urls = (
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:list', None),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:success', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
