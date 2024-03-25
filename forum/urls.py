from django.urls import path, include
# Импортируем созданное нами представление
from .views import PostList, PostSearch, PostCreate, PostUpdate, PostDelete, CategoryListView, PostDetail
from django.views.decorators.cache import cache_page




urlpatterns = [
   path('', cache_page(5)(PostList.as_view()), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),

   path('search/', PostSearch.as_view(), name='search'),

   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),

   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
]
