# Generated by Django 2.1 on 2018-11-01 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0007_auto_20181101_1651'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='antiguedad',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='marketPrice',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='mercadoObjetivo',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='permisoEdificacionFecha',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='permisoEdificacionNo',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='permisoEdificacionSuperficie',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='selloDeGases',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='tipoPropiedad',
        ),
        migrations.RemoveField(
            model_name='apartment',
            name='vidaUtil',
        ),
    ]
