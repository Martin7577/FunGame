from django_filters import FilterSet
from django.forms import DateInput
from .models import Post, Category
from django import forms
import django_filters


class PostFilter(FilterSet):
    # title = django_filters.Filter(field_name='header', lookup_expr='icontains', label='Название')
    # time = django_filters.DateFilter(field_name='time_in', lookup_expr='gte', widget=DateInput(attrs={'type': 'date'}), label='С')
    # category = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={'category': 'category'}), label = 'Категория')
    # author = django_filters.Filter(field_name='post_author', lookup_expr='icontains', label='Автор')
    # text = django_filters.Filter(field_name='text_post', lookup_expr='icontains', label='Содержание')
    class Meta:
        model = Post
        fields = {
            'category',
            'post_author',
            'header',
            'time_in',
            'text',
        }