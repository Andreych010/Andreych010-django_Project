from django.db import models

NULLABLE = {'null': True, 'blank': True}


class BlogPost(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    body = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog_post/', verbose_name='изображение', **NULLABLE)
    date_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    sign_publication = models.BooleanField(verbose_name='признак публикации')
    number_views = models.IntegerField(verbose_name='количество просмотров', **NULLABLE)

    def __str__(self):
        return f'{self.title}, {self.slug}, {self.body}, {self.preview},' \
               f'{self.date_creation}, {self.sign_publication}, {self.number_views}'

    class Meta:
        verbose_name = 'наименование'
        verbose_name_plural = 'Blog'
        ordering = ('id',)
