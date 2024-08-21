from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import os

from products.models import Product


class Command(BaseCommand):
    help = 'Парсинг изображений с сайта и сохранение в базу данных'

    def handle(self, *args, **kwargs):
        url = 'https://www.ozon.ru/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')

            folder = 'data/images'
            if not os.path.exists(folder):
                os.makedirs(folder)

            for index, img in enumerate(images):
                img_url = img['src']  # Получаем URL изображения
                img_data = requests.get(img_url).content  # Скачиваем изображение
                
                # Генерация имени файла из тега
                name_tag = img.get('alt')
                if name_tag:
                    name_tag = name_tag if len(name_tag) < 20 else name_tag[:20]
                    name_tag.replace('/', '-')

                    # Определяем имя файла для сохранения
                    file_name = f'{name_tag}_{index + 1}.jpg'
                    file_path = os.path.join(folder, file_name)
                    
                    # Сохраняем изображение на диск
                    with open(file_path, 'wb') as handler:
                        handler.write(img_data)
                    
                    # Сохраняем информацию в базу данных через Django ORM
                    try:
                        product_image = Product(name=name_tag, image=file_path)
                        product_image.save()
                    except Exception:
                        print('Problem saving to db')
                    
                    print(f'{file_name} сохранено и добавлено в базу данных.')
        else:
            print(f'Ошибка при запросе страницы: {response.status_code}')

