from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db.models.signals import post_save
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product
from products.signals import save_image_features


class SearchSimilarTests(APITestCase):
    def setUp(self):
        '''Loads data dumped from the actual database, as required for the test.'''

        self.path = reverse('products:products-search')
        
        post_save.disconnect(receiver=save_image_features, sender=Product)
        call_command('loaddata', 'initial_data.json')
        post_save.connect(receiver=save_image_features, sender=Product)
        
    def test_correct_search(self):
        image_path = 'core/products/tests/test_data/krossovki.jpeg'
        with open(image_path, 'rb') as image_file:
            image = SimpleUploadedFile(
                name='test-krossovki.jpeg',
                content=image_file.read(),
                content_type='image/jpeg'
            )

        response = self.client.post(
            path=self.path,
            data={'image': image},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
