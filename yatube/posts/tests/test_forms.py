from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus

from posts.models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=('Заголовок для тестовой группы'),
            slug='test_slug5',
            description='Тестовое описание'
        )
        cls.user = User.objects.create_user(username='Nikita')

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post(self):
        count_posts = Post.objects.count()
        form_data = {
            'text': 'Данные из формы',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        post_1 = Post.objects.first()
        self.assertEqual(Post.objects.count(), count_posts + 1)
        self.assertRedirects(response, reverse(
            'posts:profile', args=(self.user.username,)))
        self.assertEqual(post_1.author, self.user)
        self.assertEqual(post_1.text, form_data['text'])
        self.assertEqual(post_1.group.id, form_data['group'])

    def test_guest_new_post(self):
        """неавторизоанный не может создавать посты"""
        count_posts_1 = Post.objects.count()
        form_data = {
            'text': 'Пост от неавторизованного пользователя',
            'group': self.group.id
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertFalse(Post.objects.filter(
            text='Пост от неавторизованного пользователя').exists())
        count_posts_2 = Post.objects.count()
        self.assertEqual(count_posts_1, count_posts_2)

    def test_authorized_edit_post(self):
        """авторизованный может редактировать"""
        form_data = {
            'text': 'Данные из формы',
            'group': self.group.id
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.first()
        form_data = {

            'text': 'Измененный текст',
            'group': self.group.id

        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post_2.id}),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.first()
        self.assertEqual(HTTPStatus.OK.value, 200)
        self.assertEqual(post_2.text, 'Измененный текст')
