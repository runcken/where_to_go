from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Place


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
                'placeId': place.id,
                'detailsUrl': reverse(
                    'place_details',
                    kwargs={'place_id': place.id}
                )
            }
        }
        features.append(feature)

    serialize_geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    return render(request, 'index.html', {'geojson_data': serialize_geojson})


def place_details(request, place_id):
    place = get_object_or_404(
        Place.objects.prefetch_related('images'),
        id=place_id
    )

    images = [(image.image.url) for image in place.images.all() if image.image]

    serialize_place = {
        'title': place.title,
        'imgs': images,
        'description_short': place.short_description,
        'description_long': place.long_description,
        'coordinates': {
            'lat': place.lat,
            'lng': place.lng
        }
    }

    return JsonResponse(
        serialize_place,
        json_dumps_params={'ensure_ascii': False}
    )
