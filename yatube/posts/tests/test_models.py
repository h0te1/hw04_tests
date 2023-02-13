from django.test import TestCase

from ..models import Group, Post, User


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост в котором больше пятнадцати символов',
        )

    def test_group_have_correct_object_names(self):
        """Проверяем, что у группы корректно работает __str__."""
        self.assertEqual(self.group.title, str(self.group))

    def test_post_have_correct_object_names(self):
        """Проверяем, что у поста корректно работает __str__."""
        self.assertEqual(self.post.text[:15], str(self.post))

# тесты для help_text и verbouse_name в теории несомненно были.
# Но были они лишь как дополнительные задания для тех,
# Кто хочет их сделать и для тех, у кого есть время.

# У меня не осталось академов, Последний спринт уже начался.
# Если я буду делать ещё и необязательные задания - меня отчислят
