import numpy as np
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from sklearn.metrics.pairwise import cosine_similarity

from .models import Product
from .serializers import ProductSerializer
from .utils.image_features import extract_features


class ProductPagination(PageNumberPagination):
    page_size = 10


class ListCreateProductsView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class SimilarImagesAPIView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        uploaded_image = request.FILES['image']
        temp_image_path = 'temp_image.jpg'
        
        with open(temp_image_path, 'wb+') as temp_file:
            for chunk in uploaded_image.chunks():
                temp_file.write(chunk)

        query_features = extract_features(temp_image_path)

        products = Product.objects.exclude(image_features__isnull=True) # Add limit?
        if not products:
            return Response(data={'error': 'No qualified products found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        all_features = [np.frombuffer(product.image_features, dtype=np.float32) for product in products]

        similarities = cosine_similarity([query_features], all_features)
        similar_indices = similarities.argsort()[0][-5:][::-1]

        similar_products = [products[int(index)] for index in similar_indices]
        serializer = ProductSerializer(similar_products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
