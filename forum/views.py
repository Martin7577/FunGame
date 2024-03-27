from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from requests import post

from .filters import PostFilter
from .forms import *
from .models import *
from django.urls import reverse_lazy
# from .tasks import send_mails, send_email_week
# from .serializers import *

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,
                  'post.html',
                  {'post': post, 'form': form, 'comment': comment})


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class PostList(ListView):
    # if request.method == "POST":
    #     handle_uploaded_file(request.FILES["file_upload"])
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = 'time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10

# class PostDetail(DetailView):
#     template_name = 'post.html'
#     context_object_name = 'post'
#     queryset = Post.objects.all()
def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(request,
                  'post.html',
                  {'post': post,'comments': comments, 'form': form})


class PostSearch(ListView):
    model = Post
    ordering = 'header'
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_create.html'
    permission_required = ('rest.add_post',)


    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     if self.request.path == '/news/articles/create/':
    #         post.type = 'A'
    #     post.save()
    #     send_mails.delay(post.pk)
    #     send_email_week.delay()
    #     return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    permission_required = ('rest.change_post',)

class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    # def get_queryset(self):
    #     self.category = get_object_or_404(Category, id=self.kwargs['pk'])
    #     queryset = Post.objects.filter(category=self.category).order_by('-time_in')
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return queryset



