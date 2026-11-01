
from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница со списком договоров и публикаций
    path('', views.archive, name='archive'),

    # Просмотр договора страхования
    path(
        'contract/<int:contract_id>/',
        views.get_contract,
        name='get_contract'
    ),

    # Создание новой публикации
    path(
        'article/new/',
        views.create_post,
        name='create_post'
    ),

    # Просмотр отдельной публикации
    path(
        'article/<int:article_id>/',
        views.get_article,
        name='get_article'
    ),
]
