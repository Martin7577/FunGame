from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from requests import post
from django.core.mail import EmailMultiAlternatives
from django.template. loader import render_to_string
from django.core.mail import send_mail

from .filters import PostFilter
from .forms import *
from .models import *
from django.urls import reverse_lazy




@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, **kwargs):
    send_mail(
    subject=f'{instance.post.user.username}, вам пришел новый отклик {instance.date.strftime("%d %m %y")}',
    message=f"на пост '{instance.post.header}' отклик от {instance.user.username}: {instance.content}",
    from_email="t1mur.yuldashev@yandex.ru",
    recipient_list=[instance.post.user.email])
    print(f' {instance.user.username} {instance.date.strftime("%d %m %Y")}')

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
                  'comment.html',
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



class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    # def get_queryset(self):
    #     self.category = get_object_or_404(Category, id=self.kwargs['pk'])
    #     queryset = Post.objects.filter(category=self.category).order_by('-time_in')
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     return queryset


class ResponseList(ListView):
    model = Comment
    template_name = 'response.html'
    context_object_name = 'respons'

def post(request):
    context = {
        'posts': Post.objects.filter(user=request.user)
    }
    return render(request, 'response.html', context)
def response(request):

    # if Comment.post.user == Post.user:
    #     return ...

    context = {
        'responses': Comment.objects.filter(user=request.user)
    }

    return render(request, 'response.html', context)

def user_posts_comments(request):
    user = request.user
    user_posts = Post.objects.filter(user=user)
    post_comments = {}
    for post in user_posts:
        post_comments[post] = post.comments.all()
    return render(request, 'response.html', {'post_comments': post_comments})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('user_posts_comments')

def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.post.user:
        comment.active = True
        comment.save()
        # Redirect back to the same page after approving the comment
        return redirect('user_posts_comments')
    else:
        # Add error handling or redirect to a different page
        pass