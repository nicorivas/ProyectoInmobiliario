# Generated by Django 2.1 on 2018-11-01 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0003_auto_20181024_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='adobe',
        ),
        migrations.RemoveField(
            model_name='house',
            name='anoConstruccion',
        ),
        migrations.RemoveField(
            model_name='house',
            name='areaUtilEdificacion',
        ),
        migrations.RemoveField(
            model_name='house',
            name='areaUtilTerreno',
        ),
        migrations.RemoveField(
            model_name='house',
            name='avaluoFiscal',
        ),
        migrations.RemoveField(
            model_name='house',
            name='builtSquareMeters',
        ),
        migrations.RemoveField(
            model_name='house',
            name='copropiedadInmobiliaria',
        ),
        migrations.RemoveField(
            model_name='house',
            name='desmontable',
        ),
        migrations.RemoveField(
            model_name='house',
            name='destinoSII',
        ),
        migrations.RemoveField(
            model_name='house',
            name='dfl2',
        ),
        migrations.RemoveField(
            model_name='house',
            name='expropiacion',
        ),
        migrations.RemoveField(
            model_name='house',
            name='ocupante',
        ),
        migrations.RemoveField(
            model_name='house',
            name='permisoEdificacion',
        ),
        migrations.RemoveField(
            model_name='house',
            name='permisoEdificacionDate',
        ),
        migrations.RemoveField(
            model_name='house',
            name='recepcionFinal',
        ),
        migrations.RemoveField(
            model_name='house',
            name='recepcionFinalDate',
        ),
        migrations.RemoveField(
            model_name='house',
            name='selloVerde',
        ),
        migrations.RemoveField(
            model_name='house',
            name='tipoBien',
        ),
        migrations.RemoveField(
            model_name='house',
            name='usoActual',
        ),
        migrations.RemoveField(
            model_name='house',
            name='usoFuturo',
        ),
        migrations.RemoveField(
            model_name='house',
            name='valorComercialUF',
        ),
        migrations.RemoveField(
            model_name='house',
            name='vidaUtilRemanente',
        ),
        migrations.RemoveField(
            model_name='house',
            name='viviendaSocial',
        ),
    ]
