# Generated by Django 2.1 on 2018-11-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0034_auto_20181119_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='permisoEdificacionFecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha permiso edificación'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='permisoEdificacionNo',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Permiso edificación'),
        ),
        migrations.AlterField(
            model_name='realestate',
            name='permisoEdificacionSuperficie',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie permiso edificación'),
        ),
    ]