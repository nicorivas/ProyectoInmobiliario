# Generated by Django 2.1 on 2019-05-13 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propertyType', models.PositiveIntegerField(choices=[('', '---------'), (1, 'Casa'), (3, 'Edificio'), (2, 'Departamento'), (8, 'Terreno'), (26, 'Parcela eriaza'), (25, 'Parcela edificada'), (6, 'Oficina'), (19, 'Casa-Oficina'), (7, 'Local comercial'), (20, 'Propiedad comercial'), (9, 'Industria'), (11, 'Bodega'), (10, 'Galpon'), (21, 'Centro educacional'), (12, 'Estacionamiento'), (14, 'Barco'), (15, 'Vehículo'), (16, 'Maquinaria'), (17, 'Estación de servicio'), (18, 'Condominio'), (22, 'Hotel'), (23, 'Motel'), (24, 'Segunda vivienda'), (0, 'Otro')], default=0)),
                ('name', models.CharField(blank=True, default='', max_length=300, verbose_name='Nombre')),
                ('marketPrice', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio mercado UF')),
                ('mercadoObjetivo', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Mercado objetivo')),
                ('anoConstruccion', models.IntegerField(blank=True, null=True, verbose_name='Año construcción')),
                ('vidaUtilRemanente', models.IntegerField(blank=True, null=True, verbose_name='Vida util remanente')),
                ('avaluoFiscal', models.FloatField(blank=True, null=True, verbose_name='Avaluo fiscal')),
                ('dfl2', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='DFL 2')),
                ('selloVerde', models.CharField(blank=True, choices=[('V', 'Verde'), ('A', 'Amarillo'), ('AV', 'Amarillo Vencido'), ('R', 'Rojo'), ('NA', 'No Aplica'), ('VV', 'Verde vencido'), ('SA', 'Sin antecedentes')], max_length=2, null=True, verbose_name='Sello verde')),
                ('copropiedadInmobiliaria', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Copropiedad Inmobiliaria')),
                ('ocupante', models.CharField(blank=True, choices=[('P', 'Propietario'), ('A', 'Arrendatario'), ('O', 'Otro'), ('SO', 'Sin ocupante')], max_length=2, null=True, verbose_name='Ocupante')),
                ('tipoBien', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tipo de bien')),
                ('destinoSII', models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud'), ('SE', 'Sitio Eriazo')], max_length=1, null=True, verbose_name='Destino según SII')),
                ('usoActual', models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud'), ('SE', 'Sitio Eriazo')], max_length=1, null=True, verbose_name='Uso actual')),
                ('usoFuturo', models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud'), ('SE', 'Sitio Eriazo')], max_length=1, null=True, verbose_name='Uso futuro')),
                ('permisoEdificacionNo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Permiso edificación')),
                ('permisoEdificacionFecha', models.DateField(blank=True, null=True, verbose_name='Fecha permiso edificación')),
                ('permisoEdificacionSuperficie', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie permiso edificación')),
                ('recepcionFinalNo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Recepcion final')),
                ('recepcionFinalFecha', models.DateField(blank=True, null=True, verbose_name='Recepcion final fecha')),
                ('expropiacion', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Expropiacion')),
                ('viviendaSocial', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Vivienda social')),
                ('desmontable', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Desmontable')),
                ('adobe', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Adobe')),
                ('acogidaLey', models.IntegerField(blank=True, choices=[(0, 'O.G.U. y C.'), (1, 'P.R.C.'), (2, 'Ley Pereira'), (3, 'Ley 19583'), (4, 'Ley 19667'), (5, 'Ley 19727'), (6, 'Ley 20251'), (7, 'Ley 6071'), (8, 'Ninguna'), (9, 'Antigüedad')], null=True, verbose_name='Acogida a')),
                ('tipoPropiedad', models.PositiveSmallIntegerField(choices=[(0, 'Usada'), (1, 'Nueva'), (3, 'No Aplica')], default=0, null=True, verbose_name='Tipo de propiedad')),
                ('antiguedad', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Antiguedad')),
                ('vidaUtil', models.PositiveSmallIntegerField(default=80, null=True, verbose_name='Vida util')),
                ('complementary', models.BooleanField(blank=True, default=False, verbose_name='Complementaria')),
                ('material', models.CharField(blank=True, choices=[('-', 'Desconocido'), ('A', 'Acero'), ('B', 'Hormigón'), ('C', 'Albañilería'), ('D', 'Piedra/Bloque'), ('E', 'Madera'), ('F', 'Adobe'), ('G', 'Metalcom'), ('H', 'Prefab. Madera'), ('I', 'Prefab. Hormigón'), ('J', 'Otros')], default='-', max_length=2)),
                ('year', models.DateField(blank=True, null=True, verbose_name='Año construcción')),
                ('quality', models.IntegerField(blank=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True, verbose_name='Calidad')),
                ('state', models.IntegerField(blank=True, choices=[(1, 'Sin valor'), (2, 'Malo'), (3, 'Regular'), (4, 'Bueno'), (5, 'Muy bueno')], null=True, verbose_name='Estado')),
                ('prenda', models.BooleanField(blank=True, choices=[(None, 'S/A'), (True, 'Si'), (False, 'No')], null=True, verbose_name='Mercado objetivo')),
                ('recepcion', models.IntegerField(blank=True, choices=[(0, 'Con R/F'), (1, 'Sin R/F'), (2, 'Sin P/E'), (3, 'Sin Ant.'), (4, 'N/R')], default=4)),
                ('area', models.FloatField(blank=True, null=True, verbose_name='Area')),
                ('UFPerArea', models.FloatField(blank=True, default=0, verbose_name='Area density')),
                ('real_estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.RealEstate', verbose_name='Real estate')),
            ],
        ),
    ]
