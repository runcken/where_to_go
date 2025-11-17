import json
import os

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from urllib.parse import urlparse

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Load place data from JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            type=str,
            help='URL or path to JSON file'
        )
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
            serialize_place = self.load_json_data(json_url)

            title = serialize_place.get('title', 'Неизвестное место')
            self.stdout.write(f'Загружаем данные для: {title}')

            lng = serialize_place['coordinates']['lng']
            lat = serialize_place['coordinates']['lat']

            if not update_existing:
                existing_place = Place.objects.filter(
                    title=title,
                    lng=lng,
                    lat=lat
                ).first()
                if existing_place:
                    self.stdout.write(
                        self.style.WARNING(f'Место {title} уже существует. \
                            Используйте --update для перезаписи')
                    )
                    return

            place, created = Place.objects.update_or_create(
                title=title,
                lng=lng,
                lat=lat,
                defaults={
                    'short_description': serialize_place.get(
                        'description_short', ''
                    ),
                    'long_description': serialize_place.get(
                        'description_long', ''
                    ),
                }
            )

            action = 'Создано' if created else 'Обновлено'
            self.stdout.write(
                f'Место {place.title} {action} (ID: {place.id})'
            )

            if 'imgs' in serialize_place:
                if clear_images:
                    deleted_count, _ = place.images.all().delete()
                    self.stdout.write(
                        f'Удалено {deleted_count} старых изображений'
                    )

                self.download_images(place, serialize_place['imgs'])

            self.stdout.write(
                self.style.SUCCESS(
                    f'Успешно загружено место: {title} (ID: {place.id})'
                )
            )

        except Exception as e:
            self.stderr.write(f"Ошибка при загрузке данных: {str(e)}")
            raise e

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
                    self.stdout.write(f'  Пропущен локальный файл: {img_url}')
                    continue

                response = requests.get(img_url, timeout=30)
                response.raise_for_status()

                parsed_url = urlparse(img_url)
                filename = os.path.basename(parsed_url.path)

                if not os.path.splitext(filename)[1]:
                    filename += '.jpg'

                unique_filename = f'{place.id}_{order}_{filename}'

                PlaceImage.objects.create(
                    place=place,
                    order=order,
                    image=ContentFile(response.content, name=unique_filename)
                )

                self.stdout.write(
                    f'  Загружено изображение: {unique_filename}'
                )

            except requests.exceptions.RequestException as e:
                self.stderr.write(
                    f'  Ошибка сети при загрузке {img_url}: {str(e)}'
                )
            except Exception as e:
                self.stderr.write(
                    f'  Ошибка при загрузке изображения {img_url}: {str(e)}'
                )
