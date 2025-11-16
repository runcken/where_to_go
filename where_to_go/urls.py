from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from places import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', views.index, name='index'),
    path('places/<slug:place_id>/', views.place_details, name='place_details'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
