from django import forms
from django.core.exceptions import ValidationError
from datetime import date
from .models import Post, Category, Comment



class PostForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'category': 'category'}), label = 'Категория')
    class Meta:
        model = Post
        fields = ['header', 'text', 'post_author', 'category', 'image']

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'content']

