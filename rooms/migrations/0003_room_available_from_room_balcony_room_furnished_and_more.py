# Generated by Django 4.2.1 on 2023-05-13 14:26

from django.db import migrations, models
import django.utils.timezone
import rooms.models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_alter_room_garden_alter_room_house_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='available_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='room',
            name='balcony',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='furnished',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='pets',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='floor',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='garden',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='parking',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AlterField(
            model_name='roomimage',
            name='image',
            field=models.ImageField(default='room_pics/default.jpg', upload_to=rooms.models.RoomImage.get_upload_path),
        ),
    ]
