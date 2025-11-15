from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.http import JsonResponse
from django.urls import reverse
import json
from .models import Place


def show_main(request):
    return render(request, 'index.html')


def index(request):
    places = Place.objects.prefetch_related('images').all()

    features = []
    for place in places:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [place.lng, place.lat]
            },
            'properties': {
                'title': place.title,
                'placeId': place.place_id,
                'detailsUrl': reverse('place_details', kwargs={'place_id': place.place_id})
            }
        }
        features.append(feature)

    geojson_data = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return render(request, 'index.html', {'geojson_data': geojson_data})


def place_details(request, place_id):
    place = get_object_or_404(Place, place_id=place_id)

    images = []
    for image in place.images.all():
        if image.image:
            images.append(image.image.url)

    place_data = {
        'title': place.title,
        'imgs': images,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lng
        }
    }

    return JsonResponse(place_data, json_dumps_params={'ensure_ascii': False})
