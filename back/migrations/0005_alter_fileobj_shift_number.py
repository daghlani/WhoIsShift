# Generated by Django 3.2 on 2022-01-11 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0004_fileobj_shift_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileobj',
            name='shift_number',
            field=models.IntegerField(verbose_name='تلفن شیفت'),
        ),
    ]
