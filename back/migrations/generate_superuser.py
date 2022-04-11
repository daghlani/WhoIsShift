# Generated by Django 3.2 on 2022-03-16 13:52
from django.contrib.auth.models import User
from django.db import migrations


def generate_superuser(apps, schema_editor):
    import os
    from django.contrib.auth.models import User

    DJANGO_SU_NAME = os.environ.get('DJANGO_SU_NAME', 'admin')
    DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', 'admin@local.com')
    DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', 'admin')

    superuser = User.objects.create_superuser(
        username=DJANGO_SU_NAME,
        email=DJANGO_SU_EMAIL,
        password=DJANGO_SU_PASSWORD)

    superuser.save()


def revert(apps, schema_editor):
    User.objects.filter(username='admin').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('back', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_superuser, revert)
    ]