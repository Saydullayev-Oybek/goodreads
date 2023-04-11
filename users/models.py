from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='user_pictures', default='default_profile_o=pic.png')