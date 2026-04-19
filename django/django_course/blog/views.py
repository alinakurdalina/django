from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import News, Comment
from .forms import NewsForm, CommentForm


def home(request):
    """Главная страница"""
    latest_news = News.objects.all()[:3]
    return render(request, 'blog/home.html', {'latest_news': latest_news})


def contacts(request):
    """Страница контактов"""
    return render(request, 'blog/contacts.html')


def news_list(request):
    """Список новостей"""
    news_list_all = News.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        news_list_all = news_list_all.filter(
            Q(title__icontains=search_query) | Q(content__icontains=search_query)
        )

    sort_order = request.GET.get('sort', 'desc')
    if sort_order == 'asc':
        news_list_all = news_list_all.order_by('date_published')
    else:
        news_list_all = news_list_all.order_by('-date_published')

    paginator = Paginator(news_list_all, 10)
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)

    return render(request, 'blog/news_list.html', {
        'news_page': news_page,
        'search_query': search_query,
        'sort_order': sort_order,
    })


def news_detail(request, pk):
    """Детальная страница новости"""
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.filter(is_active=True)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.user = request.user
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('blog:news_detail', pk=news.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/news_detail.html', {
        'news': news,
        'comments': comments,
        'form': form,
    })


def is_staff_or_superuser(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff_or_superuser)
def news_create(request):
    """Создание новости"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, 'Новость создана!')
            return redirect('blog:news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'blog/news_form.html', {'form': form, 'title': 'Создать новость'})


@login_required
@user_passes_test(is_staff_or_superuser)
def news_edit(request, pk):
    """Редактирование новости"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Новость обновлена!')
            return redirect('blog:news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'blog/news_form.html', {'form': form, 'title': 'Редактировать новость'})


@login_required
@user_passes_test(is_staff_or_superuser)
def news_delete(request, pk):
    """Удаление новости"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Новость удалена!')
        return redirect('blog:news_list')
    return render(request, 'blog/news_confirm_delete.html', {'news': news})