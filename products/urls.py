from django.urls import path

from .views import ListCreateProductsView, search_similar


urlpatterns = [
    path('', ListCreateProductsView.as_view(), name='products-lc'),
    path('search/', search_similar, name='products-search')
]
