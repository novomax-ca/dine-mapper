from django.db import models
from PIL import Image
from django.conf import settings
import os
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin


class Marker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    visited_at = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='photos/thumbnails/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            width, height = img.size
            new_width, new_height = 800, 600

            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = (width + new_width) / 2
            bottom = (height + new_height) / 2

            img = img.crop((left, top, right, bottom))
            img.save(self.image.path)

            img.thumbnail((250, 187))
            thumbnail_path = self.image.path.replace('/photos/', '/photos/thumbnails/')
            img.save(thumbnail_path)
            print(thumbnail_path)
            relative_thumbnail_path = os.path.relpath(thumbnail_path, settings.MEDIA_ROOT)
            self.thumbnail = relative_thumbnail_path
            super().save(*args, **kwargs)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )