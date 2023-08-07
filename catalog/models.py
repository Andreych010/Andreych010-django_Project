from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.description}'

    class Meta:
        verbose_name = 'наименование'
        verbose_name_plural = 'Category'
        ordering = ('id',)


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='Product/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    purchase_price = models.IntegerField(verbose_name='цена товара')
    date_of_creation = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    last_modified_date = models.DateField(auto_now=True, verbose_name='Дата последнего изменения')
    active_version = models.BooleanField(verbose_name='признак текущей версии', **NULLABLE)

    def __str__(self):
        return f'{self.name}, {self.description}, {self.preview}, {self.category},' \
               f'{self.purchase_price}, {self.date_of_creation}, {self.last_modified_date}'

    class Meta:
        verbose_name = 'наименование'
        verbose_name_plural = 'Product'
        ordering = ('id',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_ver')
    number_version = models.IntegerField(verbose_name='номер версии')
    name_version = models.CharField(max_length=150, verbose_name='название версии')
    active_version = models.BooleanField(verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.number_version}, {self.name_version}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('id',)