# Generated by Django 3.2 on 2022-02-17 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0005_auto_20220217_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default=' ', max_length=30),
        ),
        migrations.AddField(
            model_name='profile',
            name='name',
            field=models.CharField(default=' ', max_length=20),
        ),
        migrations.AddField(
            model_name='shiftday',
            name='day_pr_people_list',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='shiftday',
            name='night_pr_people_list',
            field=models.TextField(default=''),
        ),
    ]