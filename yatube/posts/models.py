from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='название',
    )
    slug = models.SlugField(
        verbose_name='то, что будет в url',
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
    )

    class Meta:
        ordering = ['title']
        default_related_name = 'group'
        verbose_name = 'Группа'

    def __str__(self):
        return f'{self.title}'


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста',
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
        related_name='posts',
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относиться пост'
    )

    class Meta:
        ordering = ['-pub_date']  # Если исправить [] на (), то
        default_related_name = 'posts'  # Появится 9 ошибок в пайтесте
        verbose_name = 'пост'

    def __str__(self):
        return f'{self.text[:15]}'
