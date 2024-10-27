from django.db import migrations

from django.core.management import call_command

def load_my_initial_data(apps, schema_editor):
    call_command("loaddata", "buattalita")

class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_my_initial_data),
    ]