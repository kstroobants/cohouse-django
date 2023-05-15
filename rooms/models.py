from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
import os
from PIL import Image
from datetime import date
from django.conf import settings

class Room(models.Model):
    class House_type(models.TextChoices):
        FLAT = "F", _("Flat")
        HOUSE = "H", _("House")
        

    class YesNo(models.IntegerChoices):
        NO = 0, _("No")
        YES = 1, _("Yes")


    house_type = models.CharField(max_length=1, choices=House_type.choices)
    price = models.IntegerField()
    floor = models.IntegerField(blank=True, null=True)
    garden = models.IntegerField(choices=YesNo.choices, default=YesNo.NO)
    balcony = models.IntegerField(choices=YesNo.choices, default=YesNo.NO)
    parking = models.IntegerField(choices=YesNo.choices, default=YesNo.NO)
    furnished = models.IntegerField(choices=YesNo.choices, default=YesNo.NO)
    bathroom = models.IntegerField()
    size = models.IntegerField()
    residents = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    available_from = models.DateTimeField(default=timezone.now)

    @property
    def available_from_is_past_due(self):
        return date.today() >= self.available_from.date()
    
    def has_only_default(self, delete=False):
        if self.roomimage_set.count()==1:
            room_img_first = self.roomimage_set.first()
            if room_img_first.image.url == settings.MEDIA_URL + 'room_pics/default.jpg':
                if delete == True:
                    room_img_first.delete()
                return True
        return False



class RoomImage(models.Model):
    
    def get_upload_path(instance, filename):
        return os.path.join("room_pics/room_%d" % instance.room.id, filename)
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(default='room_pics/default.jpg', upload_to=get_upload_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img.thumbnail([600, 400], Image.ANTIALIAS) #[width, height]
        img.save(self.image.path)

