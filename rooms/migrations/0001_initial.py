# Generated by Django 4.2.1 on 2023-05-11 10:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_type', models.CharField(choices=[('FL', 'Flat'), ('HO', 'House')], max_length=2)),
                ('price', models.IntegerField()),
                ('floor', models.IntegerField()),
                ('garden', models.CharField(choices=[('NO', 'No'), ('BA', 'Balcony'), ('YE', 'Yes')], max_length=2)),
                ('parking', models.CharField(choices=[('NO', 'No'), ('RC', 'Residents card'), ('DW', 'Driveway'), ('GA', 'Garage')], max_length=2)),
                ('bathroom', models.IntegerField()),
                ('size', models.IntegerField()),
                ('description', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('residents', models.ManyToManyField(related_name='residents', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='room_pics')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.room')),
            ],
        ),
    ]
