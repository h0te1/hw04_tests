from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image',)
        help_texts = {
            'text': ('введите текст'),
            'group': ('Выберите группу для этого поста'),
            'image': ('вы можете вставить картинку'),
        }
        lables = {
            'text': ('текст'),
            'group': ('Группа')
        }


class CommentForm:
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {
            'text': ('введите текст'),
        }
        lables = {
            'text': ('текст'),
        }
