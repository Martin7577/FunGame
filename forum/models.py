
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache




class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # ratings = models.IntegerField(default = 0)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255,help_text=('category name'), unique=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ManyToManyField(Category, through='PostCategory')
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='images', null=True)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def preview(self):
       return f' {self.header} \n{self.text}'

    def __str__(self):
        return self.header

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.header} {self.category.name}'

class Comment(models.Model):
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
