from drf_spectacular.utils import (extend_schema)
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import services
from .models import Product
from .serializers import ProductSerializer
from .utils.image_features import extract_features


class ProductPagination(PageNumberPagination):
    page_size = 10


@extend_schema(tags=['Products'], description='Description')
class ListCreateProductsView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


@extend_schema(tags=['Products'], description='Description')
class SimilarImagesAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        '''Receives an image from the request, evaluates its features,
        compares those features with existing products, and returns the 5 most similar products.'''

        uploaded_image = request.FILES['image']
        if not uploaded_image:
            return Response(data={'error': 'No valid image attached.'}, status=status.HTTP_400_BAD_REQUEST)

        temp_image_path = 'temp_image.jpg'
        
        with open(temp_image_path, 'wb+') as temp_file:
            for chunk in uploaded_image.chunks():
                temp_file.write(chunk)

        query_features = extract_features(temp_image_path)

        products = services.get_qualified_products()
        if not products:
            return Response(data={'error': 'No qualified products found.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        similar_products = services.get_similar_products(products, query_features)
        serializer = ProductSerializer(similar_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
