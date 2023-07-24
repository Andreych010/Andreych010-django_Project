# myapp/management/commands/fill.py
from django.core.management import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        category_list = [
            {'name': 'Смартфон',
             'description': 'Смартфон — это умный мобильный телефон. Устройство, с помощью которого можно звонить, отправлять письма. '},
            {'name': 'Планшет',
             'description': 'Планшетный компьютер — универсальное мобильное устройство, которое может использоваться разными людьми для различных целей.'},
            {'name': 'Ноутбук',
             'description': 'Сегодня ноутбуки используются в самых разных условиях, таких как на работе, в образовании, для игр, просмотра веб-страниц, для персональных мультимедиа и для общего использования домашнего компьютера.'},
            {'name': 'Роутер',
             'description': 'Роутер (маршрутизатор) — это устройство, которое получает интернет от провайдера и передает его на устройства, подключенные к внутренней сети: на ваш смартфон, планшет, ноутбук, стационарный компьютер, игровую приставку, медиаплеер, телевизор со Smart TV.'}
        ]
        category_create = []
        for category_item in category_list:
            category_create.append(Category(**category_item))
        Category.objects.bulk_create(category_create)

        pk_1 = Category.objects.get(pk=1)
        pk_2 = Category.objects.get(pk=2)
        pk_3 = Category.objects.get(pk=3)
        pk_4 = Category.objects.get(pk=4)

        product_list = [
            {'name': 'Смартфон', 'description': 'Asus', 'category': pk_1, 'purchase_price': '15000'},
            {'name': 'Планшет', 'description': 'apple', 'category': pk_2, 'purchase_price': '690000'},
            {'name': 'Ноутбук', 'description': 'Asus', 'category': pk_3, 'purchase_price': '70000'},
            {'name': 'Роутер', 'description': 'Asus', 'category': pk_4, 'purchase_price': '3000'},
        ]

        product_create = []
        for product_item in product_list:
            product_create.append(Product(**product_item))
        Product.objects.bulk_create(product_create)
