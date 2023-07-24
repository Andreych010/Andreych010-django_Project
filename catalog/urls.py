from django.urls import path
from catalog.views import home, contacts, products, product_card, category_card
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path("contacts/", contacts, name="contacts"),
    path("products/", products, name="products"),
    path("<int:pk>/product_card/", product_card, name="product_card"),
    path("<int:pk>/category_card/", category_card, name="category_card"),
]
