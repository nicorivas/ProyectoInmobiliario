# Generated by Django 2.1.1 on 2018-09-29 21:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('realestate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('realestate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='realestate.RealEstate')),
                ('bedrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Dormitorios')),
                ('bathrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Baños')),
                ('builtSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie construida')),
                ('usefulSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie util')),
                ('generalDescription', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripcion general')),
                ('areaUtilTerreno', models.IntegerField(blank=True, default=0, null=True, verbose_name='Metros cuadrados útiles terreno')),
                ('areaUtilEdificacion', models.IntegerField(blank=True, default=0, null=True, verbose_name='Metros cuadrados útiles construccion')),
                ('valorComercialUF', models.IntegerField(blank=True, default=0, null=True, verbose_name='Valor comercial UF')),
                ('anoConstruccion', models.IntegerField(blank=True, default=0, null=True, verbose_name='Año construccion')),
                ('vidaUtilRemanente', models.IntegerField(blank=True, default=0, null=True, verbose_name='Vida util remanente')),
                ('avaluoFiscal', models.FloatField(blank=True, default=0.0, null=True, verbose_name='Avaluo fiscal')),
                ('dfl2', models.BooleanField(blank=True, default=False, null=True, verbose_name='DFL 2')),
                ('selloVerde', models.CharField(blank=True, choices=[('V', 'Verde'), ('A', 'Amarillo'), ('R', 'Rojo'), ('NA', 'No Aplica'), ('VV', 'Verde vencido'), ('SA', 'Sin antecedentes')], default='SA', max_length=2, null=True, verbose_name='Sello verde')),
                ('copropiedadInmobiliaria', models.BooleanField(blank=True, default=False, null=True, verbose_name='Copropiedad Inmobiliaria')),
                ('ocupante', models.CharField(blank=True, choices=[('P', 'Propietario'), ('A', 'Arrendatario'), ('O', 'Otro'), ('SO', 'Sin ocupante')], default='P', max_length=2, null=True, verbose_name='Ocupante')),
                ('tipoBien', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Tipo de bien')),
                ('destinoSII', models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud')], default='', max_length=1, null=True, verbose_name='Destino según SII')),
                ('usoActual', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Uso actual')),
                ('usoFuturo', models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='Uso futuro')),
                ('permisoEdificacion', models.IntegerField(blank=True, default=0, null=True, verbose_name='Permiso edificación')),
                ('permisoEdificacionDate', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Permiso edificación fecha')),
                ('recepcionFinal', models.IntegerField(blank=True, default=0, null=True, verbose_name='Recepcion final')),
                ('recepcionFinalDate', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Recepcion final fecha')),
                ('expropiacion', models.BooleanField(blank=True, default=False, null=True, verbose_name='Expropiacion')),
                ('viviendaSocial', models.BooleanField(blank=True, default=False, null=True, verbose_name='Vivienda social')),
                ('adobe', models.BooleanField(blank=True, default=False, null=True, verbose_name='Construccion de adobe')),
                ('desmontable', models.BooleanField(blank=True, default=False, null=True, verbose_name='Construccion desmotanble')),
            ],
            bases=('realestate.realestate',),
        ),
    ]
