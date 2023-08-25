from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy

from blog.models import BlogPost
from catalog.forms import ProductForm, VersionForm, ModeratorForm
from catalog.models import Product, Category, Version
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django_project import settings
from django_project.settings import CACHE_ENABLED


class HomeListView(ListView):
    model = Category
    extra_context = {
        'title': 'Категории'
    }

    # def cache_example(self):
    #     if CACHE_ENABLED:
    #         # Проверяем включенность кеша
    #         key = 'category_list'  # Создаем ключ для хранения
    #         category_list = cache.get(key)  # Пытаемся получить данные
    #         if category_list is None:
    #             # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
    #             students_list = Category.objects.all()
    #             cache.set(key, category_list)
    #     else:
    #         # Если кеш не был подключен, то просто обращаемся к БД
    #         category_list = Category.objects.all()
    #     return category_list


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


class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {
        'title': 'Товары'
    }


class Product_cardDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f'version_list_{self.object.pk}'
            version_list = cache.get(key)
            if version_list is None:
                version_list = self.object.product_ver.all()
                cache.set(key, version_list)
        else:
            version_list = self.object.product_ver.all()
        context_data['versions'] = version_list
        return context_data


class Category_cardDetailView(LoginRequiredMixin, DetailView):
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin гарантирует, что только авторизованные пользователи смогут создавать новые товары
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Создание нового товара'
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
        form.instance.user = self.request.user  # Установка пользователя из request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Редактирование товара'
    }

    def get_object(self, queryset=None):
        '''
        Проверяет права доступа, если пользователь пытается редактировать не свой товар
        выкидывает ошибку Http404
        '''
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object

    def test_func(self):
        first_option = self.request.user.groups.filter(name='moderator').exists()
        second_options = self.request.user.is_superuser
        if first_option:
            self.form_class = ModeratorForm
        if second_options:
            self.form_class = ProductForm
        return first_option or second_options

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


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
    success_url = reverse_lazy('catalog:products')
    extra_context = {
        'title': 'Удаление товара'
    }
