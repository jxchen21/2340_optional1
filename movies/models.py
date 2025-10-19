from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('movie', 'user')  # One rating per user per movie
    
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name + ' (' + str(self.rating) + ' stars)'

class RegionalMoviePopularity(models.Model):
    """Track movie popularity by geographic region"""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=100)  # e.g., "Tokyo", "New York", "London"
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    purchase_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('movie', 'region_name', 'country')
        verbose_name_plural = 'Regional Movie Popularities'
    
    def __str__(self):
        return f"{self.movie.name} in {self.region_name}, {self.country} ({self.purchase_count} purchases)"
    
    @classmethod
    def update_regional_popularity(cls, movie, user_profile):
        """Update regional popularity when a movie is purchased"""
        if user_profile.city and user_profile.country and user_profile.latitude and user_profile.longitude:
            region_popularity, created = cls.objects.get_or_create(
                movie=movie,
                region_name=user_profile.city,
                country=user_profile.country,
                defaults={
                    'latitude': user_profile.latitude,
                    'longitude': user_profile.longitude,
                    'purchase_count': 1
                }
            )
            if not created:
                region_popularity.purchase_count += 1
                region_popularity.latitude = user_profile.latitude
                region_popularity.longitude = user_profile.longitude
                region_popularity.save()
    
    @classmethod
    def get_trending_movies_by_region(cls, region_name=None, country=None, limit=5):
        """Get trending movies for a specific region"""
        queryset = cls.objects.all()
        
        if region_name:
            queryset = queryset.filter(region_name__icontains=region_name)
        if country:
            queryset = queryset.filter(country__icontains=country)
        
        return queryset.order_by('-purchase_count')[:limit]
    
    @classmethod
    def get_all_regions_with_data(cls):
        """Get all regions that have movie purchase data"""
        return cls.objects.values('region_name', 'country', 'latitude', 'longitude').distinct()