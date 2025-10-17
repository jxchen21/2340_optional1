from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True, help_text="User's latitude")
    longitude = models.FloatField(null=True, blank=True, help_text="User's longitude")
    city = models.CharField(max_length=100, null=True, blank=True, help_text="User's city")
    country = models.CharField(max_length=100, null=True, blank=True, help_text="User's country")

    def __str__(self):
        return f"{self.user.username}'s profile"

    def update_location(self, lat, lng, city=None, country=None):
        """Update user's location information"""
        self.latitude = lat
        self.longitude = lng
        if city:
            self.city = city
        if country:
            self.country = country
        self.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create UserProfile when a User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Automatically save UserProfile when User is saved"""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
