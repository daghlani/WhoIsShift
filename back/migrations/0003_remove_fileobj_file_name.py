# Generated by Django 3.2 on 2022-01-09 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0002_auto_20220109_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileobj',
            name='file_name',
        ),
    ]
