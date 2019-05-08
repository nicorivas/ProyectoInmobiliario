# Generated by Django 2.1 on 2019-01-05 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('terrain', '0001_initial'),
        ('building', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=300, verbose_name='Nombre')),
                ('value', models.FloatField(blank=True, default=0, verbose_name='Valor en UF')),
            ],
        ),
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='Nombre')),
                ('addressStreet', models.CharField(blank=True, max_length=300, null=True, verbose_name='Calle')),
                ('addressNumber', models.CharField(blank=True, max_length=30, null=True, verbose_name='Número')),
                ('addressFromCoords', models.BooleanField(default=False, verbose_name='Direccion por coordenadas')),
                ('lat', models.FloatField(default=0.0, verbose_name='Latitud')),
                ('lng', models.FloatField(default=0.0, verbose_name='Longitud')),
                ('sourceUrl', models.URLField(blank=True, max_length=1000, null=True, verbose_name='Source url')),
                ('sourceName', models.CharField(blank=True, max_length=20, null=True, verbose_name='Source name')),
                ('sourceId', models.CharField(blank=True, max_length=20, null=True, verbose_name='Source id')),
                ('sourceDatePublished', models.DateTimeField(blank=True, null=True, verbose_name='Fecha publicación')),
                ('sourceAddedManually', models.BooleanField(blank=True, default=False, verbose_name='Añadido manualmente')),
                ('marketPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio mercado UF')),
                ('addressCommune', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='commune.Commune', to_field='code', verbose_name='Comuna')),
                ('addressRegion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='region.Region', to_field='code', verbose_name='Región')),
                ('assets', models.ManyToManyField(to='realestate.Asset')),
                ('buildings', models.ManyToManyField(to='building.Building')),
                ('terrains', models.ManyToManyField(to='terrain.Terrain')),
            ],
        ),
    ]
