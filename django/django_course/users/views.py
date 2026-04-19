from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import RegistrationForm, LoginForm
from blog.models import Comment


def register(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('blog:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('blog:home')
    else:
        form = RegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """Вход пользователя в систему"""
    if request.user.is_authenticated:
        return redirect('blog:home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'С возвращением, {username}!')
                next_url = request.GET.get('next', 'blog:home')
                return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя из системы"""
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('blog:home')


@login_required
def profile(request):
    """Профиль пользователя с его комментариями"""
    user_comments = Comment.objects.filter(user=request.user).select_related('news')

    return render(request, 'users/profile.html', {
        'user_comments': user_comments,
    })


@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})