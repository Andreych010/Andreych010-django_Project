from django.urls import path
from catalog.views import contacts, HomeListView, ProductsListView, Product_cardDetailView, Category_cardDetailView, \
    ProductCreateView, ProductUpdateView, ProductDeleteView
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path("contacts/", contacts, name="contacts"),
    path("products/", ProductsListView.as_view(), name="products"),
    path("view/<int:pk>/product_card/", Product_cardDetailView.as_view(), name="product_card"),
    path("<int:pk>/category_card/", Category_cardDetailView.as_view(), name="category_card"),
    path("<int:pk>/category_card/", Category_cardDetailView.as_view(), name="category_card"),
    path("blog/base/", Category_cardDetailView.as_view(), name="base_blog"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("update/<int:pk>/", ProductUpdateView.as_view(), name="product_update"),
    path("delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
]
