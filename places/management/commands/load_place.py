import os
import json
import requests
import re
from urllib.parse import urlparse
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils.text import slugify
from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Load place data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='URL or path to JSON file')
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing place if found',
        )
        parser.add_argument(
            '--clear-images',
            action='store_true',
            help='Clear existing images before adding new ones',
        )

    def handle(self, *args, **options):
        json_url = options['json_url']
        update_existing = options['update']
        clear_images = options['clear_images']
        
        try:
            place_data = self.load_json_data(json_url)
            
            title = place_data.get('title', 'Неизвестное место')
            self.stdout.write(f"Загружаем данные для: {title}")
            
            place_id = self.generate_unique_place_id(title)
            
            place, created = Place.objects.update_or_create(
                place_id=place_id,
                defaults={
                    'title': title,
                    'description_short': place_data.get('description_short', ''),
                    'description_long': place_data.get('description_long', ''),
                    'lng': place_data['coordinates']['lng'],
                    'lat': place_data['coordinates']['lat'],
                }
            )
            
            action = "создано" if created else "обновлено"
            self.stdout.write(f"Место '{place.title}' {action} (place_id: {place.place_id})")
            
            if 'imgs' in place_data:
                if clear_images:
                    deleted_count, _ = place.images.all().delete()
                    self.stdout.write(f"Удалено {deleted_count} старых изображений")
                
                self.download_images(place, place_data['imgs'])
            
            self.stdout.write(
                self.style.SUCCESS(f"Успешно загружено место: {place.title}")
            )
            
        except Exception as e:
            self.stderr.write(f"Ошибка при загрузке данных: {str(e)}")
            raise e

    def generate_unique_place_id(self, title):
        base_slug = slugify(title)
        
        if not base_slug:
            base_slug = "place"
        
        place_id = base_slug
        counter = 1
        
        while Place.objects.filter(place_id=place_id).exists():
            place_id = f"{base_slug}-{counter}"
            counter += 1
        
        return place_id

    def load_json_data(self, json_url):
        if json_url.startswith(('http://', 'https://')):
            response = requests.get(json_url)
            response.raise_for_status()
            return response.json()
        else:
            with open(json_url, 'r', encoding='utf-8') as file:
                return json.load(file)

    def download_images(self, place, image_urls):
        for order, img_url in enumerate(image_urls):
            try:
                if not img_url.startswith(('http://', 'https://')):
                    self.stdout.write(f"  Пропущен локальный файл: {img_url}")
                    continue
                
                response = requests.get(img_url, timeout=30)
                response.raise_for_status()
                
                parsed_url = urlparse(img_url)
                filename = os.path.basename(parsed_url.path)
                
                if not os.path.splitext(filename)[1]:
                    filename += '.jpg'
                
                unique_filename = f"{place.place_id}_{order}_{filename}"
                
                place_image = PlaceImage(place=place, order=order)
                
                place_image.image.save(
                    unique_filename,
                    ContentFile(response.content),
                    save=True
                )
                
                self.stdout.write(f"  Загружено изображение: {unique_filename}")
                
            except requests.exceptions.RequestException as e:
                self.stderr.write(f"  Ошибка сети при загрузке {img_url}: {str(e)}")
            except Exception as e:
                self.stderr.write(f"  Ошибка при загрузке изображения {img_url}: {str(e)}")
