# Generated by Django 2.1 on 2019-05-13 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addressNumber2', models.TextField(blank=True, max_length=30, null=True, verbose_name='Lote')),
                ('bedrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Dormitorios')),
                ('bathrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Baños')),
                ('builtSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie construida')),
                ('terrainSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie terreno')),
                ('generalDescription', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripcion general')),
                ('marketPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio mercado')),
                ('similar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='house.House')),
            ],
        ),
    ]
