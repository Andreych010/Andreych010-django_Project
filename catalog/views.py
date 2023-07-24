from django.shortcuts import render
from catalog.models import Product, Category


# from lib2to3.fixes.fix_input import context

def home(request):
    category_list = Category.objects.all()
    context = {
        'object_list': category_list,
        'title': 'Категории'
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Вам поступило новое сообщение: "{message}"\nname: {name}, phone: ({email})')
    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


def products(request):
    product_list = Product.objects.all()
    context = {
        'object_list': product_list,
        'title': 'Товары'
    }
    return render(request, 'catalog/products.html', context)


def product_card(request, pk):
    product_list = Product.objects.get(pk=pk)
    context = {
        'object': Product.objects.get(id=pk),
        'title': f'{product_list.name}'
    }
    return render(request, 'catalog/product_card.html', context)


def category_card(request, pk):
    product_list = Category.objects.get(pk=pk)
    context = {
        'object': Product.objects.get(id=pk),
        'title': f'{product_list.name}'
    }
    return render(request, 'catalog/category_card.html', context)
