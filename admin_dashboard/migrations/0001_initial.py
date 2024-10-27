# Generated by Django 5.1.1 on 2024-10-27 10:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RestaurantEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_resto', models.CharField(max_length=255)),
                ('alamat', models.TextField()),
                ('jenis_kuliner', models.CharField(max_length=50)),
                ('lokasi_resto', models.CharField(max_length=10)),
                ('range_harga', models.IntegerField()),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3)),
                ('suasana', models.CharField(max_length=255)),
                ('keramaian_resto', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MenuEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama_menu', models.CharField(max_length=100)),
                ('deskripsi', models.TextField()),
                ('image_url', models.URLField()),
                ('restaurants', models.ManyToManyField(related_name='menus', to='admin_dashboard.restaurantentry')),
            ],
        ),
    ]
