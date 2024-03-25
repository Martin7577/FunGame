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
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'comment here ...',
        'rows': '4',
    }))
    class Meta:
        model = Comment
        fields = ['content']

