# Generated by Django 2.1 on 2018-10-31 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0002_auto_20181017_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='permisoEdificacion',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Permiso edificación'),
        ),
        migrations.AlterField(
            model_name='building',
            name='recepcionFinal',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Recepcion final'),
        ),
    ]
