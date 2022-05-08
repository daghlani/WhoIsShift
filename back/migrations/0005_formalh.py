# Generated by Django 3.2 on 2022-04-30 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0004_auto_20220411_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormalH',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people_list', models.TextField(default=None)),
                ('back_people_list', models.TextField(default=None)),
                ('group', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='back.shiftgroup')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]