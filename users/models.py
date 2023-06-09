from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics')
    phone_number = PhoneNumberField()
    description = models.TextField()


    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.thumbnail([300, 300], Image.ANTIALIAS)
        img.save(self.image.path)

