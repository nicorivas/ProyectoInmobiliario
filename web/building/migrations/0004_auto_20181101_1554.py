# Generated by Django 2.1 on 2018-11-01 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0003_auto_20181031_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='usoActual',
            field=models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud')], max_length=1, null=True, verbose_name='Uso actual'),
        ),
        migrations.AlterField(
            model_name='building',
            name='usoFuturo',
            field=models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud')], max_length=1, null=True, verbose_name='Uso futuro'),
        ),
    ]
