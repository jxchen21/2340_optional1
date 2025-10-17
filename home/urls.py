from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home.index'),
    path('about', views.about, name='home.about'),
    path('map', views.map_view, name='home.map'),
    path('update-location', views.update_location, name='home.update_location'),
]