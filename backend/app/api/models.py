from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    HOTEL_MANAGER = 'HOTEL MANAGER'
    GUEST = 'GUEST'
    ADMIN = 'ADMIN'

    ROLE_CHOICES = (
        (HOTEL_MANAGER, 'HOTEL MANAGER'),
        (GUEST, 'GUEST'),
        (ADMIN, 'ADMIN'),
    )

    users = models.ManyToManyField(User, related_name='roles', null=True)
    name = models.CharField(max_length=100, unique=True, choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


# Owner Profile for more data for the owner
class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    date_of_birth = models.DateField(null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)

    def __str__(self):
        return self.user_id.username + "'s profile"
