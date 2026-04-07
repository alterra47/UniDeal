"""
Data migration to create the hardcoded admin user.
Admin credentials: admin / admin123
"""
from django.db import migrations


def create_admin(apps, schema_editor):
    Admin = apps.get_model('marketplace', 'Admin')
    import bcrypt
    password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    Admin.objects.get_or_create(
        username='admin',
        defaults={'password': password}
    )


def remove_admin(apps, schema_editor):
    Admin = apps.get_model('marketplace', 'Admin')
    Admin.objects.filter(username='admin').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_admin, remove_admin),
    ]
