
from django.shortcuts import render, redirect
from django.http import Http404
from .models import Contract, Article


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
