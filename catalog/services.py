from django.core.cache import cache
from django.shortcuts import render

from catalog.models import Category
from django_project.settings import CACHE_ENABLED


def get_category_view(request):
    if CACHE_ENABLED:
        # Проверяем включенность кеша
        key = 'category_list'  # Создаем ключ для хранения
        category_list = cache.get(key)  # Пытаемся получить данные
        if category_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        category_list = Category.objects.all()

    context = {
        'object_list': category_list,
        'title': 'Категории товаров'
        }
    return render(request, 'catalog/category_list.html', context)
