from django.shortcuts import render

from blog.models import BlogPost
from catalog.models import Product, Category
from django.views.generic import ListView, DetailView, CreateView


class HomeListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории'
    }


# class ContactView(TemplateView):
#     template_name = 'catalog/contacts.html'
#     extra_context = {
#         'title': 'Контакты'
#     }
#
#     def get_context_data(self, **kwargs):
#         if self.request.method == 'POST':
#             name = self.request.POST.get('name')
#             email = self.request.POST.get('email')
#             message = self.request.POST.get('message')
#             print(f'Вам поступило новое сообщение: "{message}"\nname: {name}, phone: ({email})')
#         return super().get_context_data(**kwargs)


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


class ProductsListView(ListView):
    model = Product
    extra_context = {
        'title': 'Товары'
    }


class Product_cardDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_item = Product.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{product_item.name}'
        return context_data


class Category_cardDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{product_item.name}'
        return context_data


class BaseListView(ListView):
    model = BlogPost
    template_name = 'blog/base.html'
    extra_context = {
        'title': 'Блог'
    }


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'slug', 'body', 'preview', 'sign_publication', 'number_views',)
