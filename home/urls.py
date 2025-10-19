from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('map', views.map_view, name='home.map'),
    path('update-location', views.update_location, name='home.update_location'),
    path('region-trending-movies', views.get_region_trending_movies, name='home.region_trending_movies'),
    path('debug-map-data', views.debug_map_data, name='home.debug_map_data'),
]