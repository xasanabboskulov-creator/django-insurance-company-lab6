
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Contract, Article


# Главная страница: архив договоров и публикации
def archive(request):
    contracts = Contract.objects.select_related(
        'client',
        'agent',
        'branch',
        'insurance_type'
    ).all()

    articles = Article.objects.select_related('author').all()

    return render(request, 'archive.html', {
        'contracts': contracts,
        'articles': articles
    })


# Просмотр отдельного договора
def get_contract(request, contract_id):
    try:
        contract = Contract.objects.select_related(
            'client',
            'agent',
            'branch',
            'insurance_type'
        ).get(id=contract_id)

        return render(request, 'article.html', {
            'post': contract
        })

    except Contract.DoesNotExist:
        raise Http404


# Просмотр отдельной публикации
def get_article(request, article_id):
    try:
        article = Article.objects.select_related('author').get(
            id=article_id
        )

        return render(request, 'post_detail.html', {
            'post': article
        })

    except Article.DoesNotExist:
        raise Http404


# Создание публикации
def create_post(request):
    if request.user.is_anonymous:
        raise Http404

    errors = []

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        text = request.POST.get('text', '').strip()

        if not title:
            errors.append('Введите название публикации.')

        if not text:
            errors.append('Введите текст публикации.')

        if title and Article.objects.filter(title=title).exists():
            errors.append(
                'Публикация с таким названием уже существует.'
            )

        if not errors:
            article = Article.objects.create(
                title=title,
                text=text,
                author=request.user
            )

            return redirect(
                'get_article',
                article_id=article.id
            )

    return render(request, 'create_post.html', {
        'errors': errors,
        'title': request.POST.get('title', ''),
        'text': request.POST.get('text', '')
    })


# Регистрация нового пользователя
def register(request):
    errors = []

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        if not username:
            errors.append('Введите логин.')

        if not email:
            errors.append('Введите электронную почту.')

        if not password:
            errors.append('Введите пароль.')

        if not password_confirm:
            errors.append('Подтвердите пароль.')

        if username and User.objects.filter(username=username).exists():
            errors.append(
                'Пользователь с таким логином уже существует.'
            )

        if password and password_confirm and password != password_confirm:
            errors.append('Пароли не совпадают.')

        if not errors:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect('login')

    return render(request, 'register.html', {
        'errors': errors,
        'username': request.POST.get('username', ''),
        'email': request.POST.get('email', '')
    })


# Авторизация пользователя
def user_login(request):
    errors = []

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username:
            errors.append('Введите логин.')

        if not password:
            errors.append('Введите пароль.')

        if not errors:
            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('archive')
            else:
                errors.append(
                    'Неверный логин или пароль.'
                )

    return render(request, 'login.html', {
        'errors': errors,
        'username': request.POST.get('username', '')
    })


# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect('archive')
