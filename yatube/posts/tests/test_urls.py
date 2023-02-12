from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def pages_response_template(self):
        template_response_code = {
            reverse('/'): 'posts/index.html',
            reverse('/group/<slug:slug>/'): 'posts/group_list.html',
            reverse('/profile/<str:username>/'): 'posts/profile.html',
            reverse('/posts/<int:post_id>/'): 'posts/post_detail.html',
            reverse('/posts/<post_id>/edit/'): 'posts/create_post.html',
            reverse('/create/'): 'posts/create_post.html',
        }
        for address, template in template_response_code.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(template)
                self.assertTemplateUsed(response, address)

    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_unexisting_page_404(self):
        """Страница /unexisting_page/ возвращает 404."""
        response = self.client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)
