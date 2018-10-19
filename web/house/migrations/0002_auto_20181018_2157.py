# Generated by Django 2.1 on 2018-10-19 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número'),
        ),
        migrations.AddField(
            model_name='house',
            name='terraceSquareMeters',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie terraza'),
        ),
    ]
