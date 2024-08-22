import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .models import Product


def get_qualified_products(): 
    products = Product.objects.exclude(image_features__isnull=True) # Add limit?
    return products

def get_similar_products(products, query_features): 
    all_features = [np.frombuffer(product.image_features, dtype=np.float32) for product in products]

    similarities = cosine_similarity([query_features], all_features)
    similar_indices = similarities.argsort()[0][-5:][::-1]

    similar_products = [products[int(index)] for index in similar_indices]
    return similar_products
