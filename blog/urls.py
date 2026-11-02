
from django.contrib import admin
from django.urls import path
from articles import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница
    path('', views.archive, name='archive'),

    # Просмотр договора
    path('contract/<int:contract_id>/', views.get_contract, name='get_contract'),

    # Публикации страховой компании
    path('article/new/', views.create_post, name='create_post'),
    path('article/<int:article_id>/', views.get_article, name='get_article'),

    # Регистрация и авторизация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
