from django.urls import path

from .views import ListCreateProductsView, SimilarImagesAPIView

app_name = 'products'

urlpatterns = [
    path('', ListCreateProductsView.as_view(), name='products-lc'),
    path('search/', SimilarImagesAPIView.as_view(), name='products-search')
]
