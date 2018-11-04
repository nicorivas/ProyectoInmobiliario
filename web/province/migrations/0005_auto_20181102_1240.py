# Generated by Django 2.1 on 2018-11-02 15:40

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commune', '0005_auto_20181102_1240'),
        ('province', '0004_provincesmall'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProvinceFull',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('code', models.PositiveSmallIntegerField(unique=True, verbose_name='Code')),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.RemoveField(
            model_name='provincesmall',
            name='region',
        ),
        migrations.RemoveField(
            model_name='province',
            name='mpoly',
        ),
        migrations.DeleteModel(
            name='ProvinceSmall',
        ),
    ]