from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group, User
from posts.forms import PostForm


def context_help(otvet, post=False):
    if post is False:
        return otvet.context.get('page_obj')[0]
    else:
        return otvet.context.get('post')


class PostTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Заголовок группы',
            slug='test_slug'
        )
        cls.user = User.objects.create_user(username='test_user')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # проверяет контекст на главной странице
    def test_context_index(self):
        """Контекст в index"""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = context_help(otvet=response)
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовая запись')
        self.assertEqual(post_author_0, 'test_user')
        self.assertEqual(post_group_0, 'Заголовок группы')

    # Проверяет контекст на странице групп
    def test_context_group_list(self):
        """Контекст в group_list"""
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,)))
        first_object = context_help(otvet=response)
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_group_0 = first_object.group.title
        self.assertEqual(post_text_0, 'Тестовая запись')
        self.assertEqual(post_author_0, 'test_user')
        self.assertEqual(post_group_0, 'Заголовок группы')
        self.assertEqual(response.context.get('group').title,
                         'Заголовок группы')
        self.assertEqual(response.context.get('group').slug, 'test_slug')

    # Проверяет контекст на странице профиля
    def test_context_profile(self):
        """Контекст в profile"""
        response = self.authorized_client.get(
            reverse('posts:profile', args=(self.user.username,)))

        first_object = context_help(otvet=response)
        post_text_0 = first_object.text
        self.assertEqual(response.context.get('author').username, 'test_user')
        self.assertEqual(post_text_0, 'Тестовая запись')

    # Проверяет содержимое страницы с деталями поста
    def test_post_detail(self):
        """тест на работоспособность post_detail"""
        response = self.authorized_client.get((
            reverse('posts:post_detail', args=(self.post.id,))
        ))
        page_obj = context_help(otvet=response, post=True)
        text = page_obj.text
        obrazec = Post.objects.get(id=1)
        self.assertEqual(text, obrazec.text)

    # правильность типов полей формы для редактирования и создания поста
    def test_post_edit_context(self):
        """Шаблон редактирования и создания поста"""
        edit_and_create = {
            ('posts:post_edit', (self.post.id,)),
            ('posts:post_create', None)
        }
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for name, args in edit_and_create:
            with self.subTest(name=name):
                response = self.authorized_client.get(reverse(name, args=args))
                form_form = response.context.get('form')
                self.assertIn('form', response.context)
                self.assertIsInstance(form_form, PostForm)
                for value, expected in form_fields.items():
                    with self.subTest(value=value):
                        form_field = response.context.get(
                            'form').fields.get(value)
                        self.assertIsInstance(form_field, expected)

    # Пост не попал в другую группу
    def test_post_another_group(self):
        """Пост не попал в другую группу"""
        Group.objects.create(
            title='Вторая группа',
            slug='test_slug_2'
        )
        response = self.authorized_client.get(
            reverse('posts:group_list', args=('test_slug_2',)))

        self.assertEqual(
            len(response.context.get('page_obj').object_list), 0)

        post = self.post
        self.assertTrue(post.group)
        response = self.authorized_client.get(
            reverse('posts:group_list', args=('test_slug',)))
        group_post = context_help(otvet=response)
        self.assertEqual(post, group_post)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='user',
                                              email='test@gmail.com',)
        cls.group = Group.objects.create(
            title=('Заголовок тестовой группы'),
            slug='test_slug',
            description='Тестовое описание')
        cls.posts = []
        for number in range(13):
            cls.posts.append(Post(
                text=f'Тестовый пост {number}',
                author=cls.author,
                group=cls.group
            )
            )
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        self.user = User.objects.create_user(username='mobpsycho100')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator(self):
        """Проверка обеих страниц паджинатора"""
        list_urls = (
            ("posts:index", None,),
            ("posts:group_list", ("test_slug",)),
            ("posts:profile", ("user",)),
        )
        pages = (
            ('?page=1', 10),
            ('?page=2', 3)
        )
        for name, args in list_urls:
            with self.subTest(url=name):
                for page, lenght in pages:
                    response = self.authorized_client.get(
                        reverse(name, args=args) + page)
                    self.assertEqual(
                        len(response.context.get('page_obj').object_list
                            ), lenght)
