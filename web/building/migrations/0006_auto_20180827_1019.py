# Generated by Django 2.1 on 2018-08-27 13:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0005_auto_20180825_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='adobe',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Construccion de adobe'),
        ),
        migrations.AddField(
            model_name='building',
            name='anoConstruccion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Año construccion'),
        ),
        migrations.AddField(
            model_name='building',
            name='avaluoFiscal',
            field=models.FloatField(blank=True, default=0.0, null=True, verbose_name='Avaluo fiscal'),
        ),
        migrations.AddField(
            model_name='building',
            name='copropiedadInmobiliaria',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Copropiedad Inmobiliaria'),
        ),
        migrations.AddField(
            model_name='building',
            name='desmontable',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Construccion desmotanble'),
        ),
        migrations.AddField(
            model_name='building',
            name='destinoSII',
            field=models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud')], default='', max_length=1, null=True, verbose_name='Destino según SII'),
        ),
        migrations.AddField(
            model_name='building',
            name='dfl2',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='DFL 2'),
        ),
        migrations.AddField(
            model_name='building',
            name='expropiacion',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Expropiacion'),
        ),
        migrations.AddField(
            model_name='building',
            name='ocupante',
            field=models.CharField(blank=True, choices=[('P', 'Propietario'), ('A', 'Arrendatario'), ('O', 'Otro'), ('SO', 'Sin ocupante')], default='P', max_length=2, null=True, verbose_name='Ocupante'),
        ),
        migrations.AddField(
            model_name='building',
            name='permisoEdificacion',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Permiso edificación'),
        ),
        migrations.AddField(
            model_name='building',
            name='permisoEdificacionDate',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Permiso edificación fecha'),
        ),
        migrations.AddField(
            model_name='building',
            name='recepcionFinal',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Recepcion final'),
        ),
        migrations.AddField(
            model_name='building',
            name='recepcionFinalDate',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Recepcion final fecha'),
        ),
        migrations.AddField(
            model_name='building',
            name='selloVerde',
            field=models.CharField(blank=True, choices=[('V', 'Verde'), ('A', 'Amarillo'), ('R', 'Rojo'), ('NA', 'No Aplica'), ('VV', 'Verde vencido'), ('SA', 'Sin antecedentes')], default='SA', max_length=2, null=True, verbose_name='Sello verde'),
        ),
        migrations.AddField(
            model_name='building',
            name='tipoBien',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Tipo de bien'),
        ),
        migrations.AddField(
            model_name='building',
            name='usoActual',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Uso actual'),
        ),
        migrations.AddField(
            model_name='building',
            name='usoFuturo',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Uso futuro'),
        ),
        migrations.AddField(
            model_name='building',
            name='vidaUtilRemanente',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Vida util remanente'),
        ),
        migrations.AddField(
            model_name='building',
            name='viviendaSocial',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Vivienda social'),
        ),
    ]
