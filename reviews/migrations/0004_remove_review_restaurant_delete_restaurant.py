# Generated by Django 5.1.2 on 2024-10-23 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_review_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='restaurant',
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
