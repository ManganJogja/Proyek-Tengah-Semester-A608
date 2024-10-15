# Generated by Django 5.1.1 on 2024-10-15 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReserveEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('tanggal_kedatangan', models.DateField()),
                ('waktu_kedatangan', models.CharField(choices=[('08:00', '08:00 AM'), ('09:00', '09:00 AM'), ('10:00', '10:00 AM'), ('11:00', '11:00 AM'), ('12:00', '12:00 PM'), ('13:00', '01:00 PM'), ('14:00', '02:00 PM'), ('15:00', '03:00 PM'), ('16:00', '04:00 PM')], max_length=5)),
                ('jumlah_tamu', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('no_telp', models.IntegerField()),
                ('notes', models.CharField(max_length=255)),
            ],
        ),
    ]
