from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import BlogPost


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'body', 'preview', 'sign_publication',)
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Создание нового блога'
    }

    def form_valid(self, form):
        '''
        при создании динамически формирует slug name для заголовка
        '''
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ('title', 'body', 'preview', 'sign_publication',)
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Редактирование блога'
    }

    def form_valid(self, form):
        '''
        при создании динамически формирует slug name для заголовка
        '''
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:list')
    extra_context = {
        'title': 'Удаление блога'
    }


class BlogPostListView(ListView):
    model = BlogPost
    extra_context = {
        'title': 'Блоговые записи'
    }

    def get_queryset(self, *args, **kwargs):
        '''
        выводить в список статей только те,
        которые имеют положительный признак публикации
        '''
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(sign_publication=True)
        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        '''
        счетчик просмотров
        '''
        self.object = super().get_object(queryset)
        self.object.number_views += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        product_item = BlogPost.objects.get(pk=self.kwargs.get('pk'))
        context_data['title'] = f'{product_item.title}'
        return context_data
