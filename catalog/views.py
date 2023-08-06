from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from prompt_toolkit.validation import ValidationError

from blog.models import BlogPost
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Category, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class HomeListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории'
    }


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'Вам поступило новое сообщение: "{message}"\nname: {name}, email: ({email})')
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Создание нового товара'
    }


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Редактирование товара'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Удаление товара'
    }
