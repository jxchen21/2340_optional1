from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
from accounts.models import UserProfile
from movies.models import RegionalMoviePopularity

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

    # Get regional movie popularity data
    regional_data = list(RegionalMoviePopularity.get_all_regions_with_data())
    
    # Get trending movies for user's region if available
    user_trending_movies = []
    if user_location and user_location['city']:
        user_trending_movies = RegionalMoviePopularity.get_trending_movies_by_region(
            region_name=user_location['city'],
            country=user_location['country'],
            limit=5
        )

    return render(request, 'home/map.html', {
        'template_data': template_data,
        'user_location': user_location,
        'regional_data': regional_data,
        'user_trending_movies': user_trending_movies,
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

@login_required
@csrf_exempt
@require_http_methods(["GET"])
def get_region_trending_movies(request):
    """Get trending movies for a specific region via AJAX"""
    try:
        region_name = request.GET.get('region')
        country = request.GET.get('country')
        
        if not region_name:
            return JsonResponse({
                'success': False,
                'message': 'Region name is required'
            }, status=400)
        
        trending_movies = RegionalMoviePopularity.get_trending_movies_by_region(
            region_name=region_name,
            country=country,
            limit=10
        )
        
        movies_data = []
        for movie_popularity in trending_movies:
            movies_data.append({
                'movie_name': movie_popularity.movie.name,
                'purchase_count': movie_popularity.purchase_count,
                'movie_id': movie_popularity.movie.id,
                'movie_price': movie_popularity.movie.price,
                'movie_image': movie_popularity.movie.image.url if movie_popularity.movie.image else None
            })
        
        return JsonResponse({
            'success': True,
            'region': region_name,
            'country': country or 'Unknown',
            'trending_movies': movies_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error getting trending movies: {str(e)}'
        }, status=500)

@login_required
def debug_map_data(request):
    """Debug endpoint to check map data"""
    try:
        regional_data = list(RegionalMoviePopularity.get_all_regions_with_data())
        
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
        
        return JsonResponse({
            'success': True,
            'api_key_configured': bool(settings.GOOGLE_MAPS_API_KEY),
            'api_key_length': len(settings.GOOGLE_MAPS_API_KEY) if settings.GOOGLE_MAPS_API_KEY else 0,
            'regional_data_count': len(regional_data),
            'regional_data': regional_data[:5],  # First 5 items
            'user_location': user_location,
            'user_authenticated': request.user.is_authenticated
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)