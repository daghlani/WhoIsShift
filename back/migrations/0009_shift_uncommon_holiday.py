# Generated by Django 3.2 on 2022-02-19 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0008_auto_20220219_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='uncommon_holiday',
            field=models.TextField(blank=True, null=True),
        ),
    ]