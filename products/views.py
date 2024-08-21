from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
# from django.views.decorators.csrf import csrf_exempt

from . import services
from .models import Product
from .serializers import ProductSerializer


class ProductPagination(PageNumberPagination):
    page_size = 10  # Количество объектов на странице
    # page_size_query_param = 'page_size'
    # max_page_size = 100  # Максимальное количество объектов на странице


class ListCreateProductsView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


# @csrf_exempt
@api_view(['POST'])
def search_similar(request):
    file = request.Files
    features = services.get_features(file)
    similar_products = services.get_similar_products(features)
    serializer = ProductSerializer(data=similar_products)
    serializer.is_valid(raise_exception=True) # mb is not required since data comes from the DB

    return Response(data=serializer.validated_data, status=status.HTTP_200_OK)
