from django.core.management.base import BaseCommand
from movies.models import Movie, RegionalMoviePopularity
import random

class Command(BaseCommand):
    help = 'Populate sample regional movie popularity data'

    def handle(self, *args, **options):
        # Sample regions with coordinates
        regions = [
            {'name': 'Tokyo', 'country': 'Japan', 'lat': 35.6762, 'lng': 139.6503},
            {'name': 'New York', 'country': 'USA', 'lat': 40.7128, 'lng': -74.0060},
            {'name': 'London', 'country': 'UK', 'lat': 51.5074, 'lng': -0.1278},
            {'name': 'Paris', 'country': 'France', 'lat': 48.8566, 'lng': 2.3522},
            {'name': 'Sydney', 'country': 'Australia', 'lat': -33.8688, 'lng': 151.2093},
            {'name': 'Toronto', 'country': 'Canada', 'lat': 43.6532, 'lng': -79.3832},
        ]

        # Get all movies
        movies = Movie.objects.all()
        
        if not movies.exists():
            self.stdout.write(
                self.style.WARNING('No movies found. Please add some movies first.')
            )
            return

        # Create sample regional popularity data
        created_count = 0
        for movie in movies:
            for region in regions:
                # Random purchase count between 1 and 50
                purchase_count = random.randint(1, 50)
                
                regional_popularity, created = RegionalMoviePopularity.objects.get_or_create(
                    movie=movie,
                    region_name=region['name'],
                    country=region['country'],
                    defaults={
                        'latitude': region['lat'],
                        'longitude': region['lng'],
                        'purchase_count': purchase_count
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    # Update existing data with random purchase count
                    regional_popularity.purchase_count = purchase_count
                    regional_popularity.latitude = region['lat']
                    regional_popularity.longitude = region['lng']
                    regional_popularity.save()

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created/updated {created_count} regional popularity records')
        )
        self.stdout.write(
            self.style.SUCCESS('Sample regional movie popularity data has been populated!')
        )
