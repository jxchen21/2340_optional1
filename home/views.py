from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
from accounts.models import UserProfile

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {
        'template_data': template_data})

def about(request):
    return render(request, 'home/about.html')

@login_required
def map_view(request):
    template_data = {}
    template_data['title'] = 'Local Popularity Map'

    # Get user's location if available
    user_location = None
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.latitude and profile.longitude:
            user_location = {
                'lat': profile.latitude,
                'lng': profile.longitude,
                'city': profile.city or 'Unknown',
                'country': profile.country or 'Unknown'
            }
    except UserProfile.DoesNotExist:
        pass

    return render(request, 'home/map.html', {
        'template_data': template_data,
        'user_location': user_location,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY
    })

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def update_location(request):
    """Update user's location via AJAX"""
    try:
        data = json.loads(request.body)
        lat = float(data.get('lat'))
        lng = float(data.get('lng'))
        city = data.get('city', '')
        country = data.get('country', '')

        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.update_location(lat, lng, city, country)

        return JsonResponse({
            'success': True,
            'message': 'Location updated successfully'
        })
    except (ValueError, KeyError, json.JSONDecodeError) as e:
        return JsonResponse({
            'success': False,
            'message': f'Invalid data: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error updating location: {str(e)}'
        }, status=500)