# Generated by Django 3.2 on 2022-02-21 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0010_shiftgroup_uncommon_holiday_req'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shiftgroup',
            options={'permissions': (('can_see_management', 'can_see_management'),)},
        ),
    ]