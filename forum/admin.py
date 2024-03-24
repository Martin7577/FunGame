from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


# class CategoryAdmin(TranslationAdmin):
#     model = Category





# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('header', 'text')  # генерируем список имён всех полей для более красивого отображения
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', )

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)

