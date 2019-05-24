# Generated by Django 2.1 on 2019-05-13 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartmentbuilding', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=300, verbose_name='Nombre')),
                ('addressNumber2', models.CharField(blank=True, max_length=30, null=True, verbose_name='Dpto.')),
                ('floor', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Piso')),
                ('bedrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Dormitorios')),
                ('bathrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Baños')),
                ('usefulSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie util')),
                ('terraceSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie terraza')),
                ('orientation', models.CharField(blank=True, choices=[('N', 'Norte'), ('NE', 'Norponiente'), ('E', 'Poniente'), ('SE', 'Surponiente'), ('S', 'Sur'), ('WS', 'Suroriente'), ('W', 'Oriente'), ('NW', 'Nororiente')], max_length=2, null=True, verbose_name='Orientación')),
                ('generalDescription', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripcion general')),
                ('programa', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Programa')),
                ('estructuraTerminaciones', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Estructura y terminaciones')),
                ('marketPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio mercado')),
                ('apartment_building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartmentbuilding.ApartmentBuilding', verbose_name='Edificio')),
                ('similar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apartment.Apartment')),
            ],
            options={
                'ordering': ['addressNumber2'],
            },
        ),
    ]
