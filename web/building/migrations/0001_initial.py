<<<<<<< HEAD
# Generated by Django 2.1.1 on 2018-09-29 21:16
=======
# Generated by Django 2.1 on 2018-09-30 12:37
>>>>>>> 24e7adb57ec744c86e5a6ec44accc51d350a96d5

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('realestate', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('realestate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='realestate.RealEstate')),
                ('sourceName', models.CharField(blank=True, max_length=20, null=True, verbose_name='Source name')),
                ('sourceUrl', models.URLField(blank=True, null=True, verbose_name='Source url')),
                ('anoConstruccion', models.IntegerField(blank=True, null=True, verbose_name='Año construccion')),
                ('vidaUtilRemanente', models.IntegerField(blank=True, null=True, verbose_name='Vida util remanente')),
                ('avaluoFiscal', models.FloatField(blank=True, null=True, verbose_name='Avaluo fiscal')),
                ('dfl2', models.BooleanField(blank=True, null=True, verbose_name='DFL 2')),
                ('selloVerde', models.CharField(blank=True, choices=[('V', 'Verde'), ('A', 'Amarillo'), ('R', 'Rojo'), ('NA', 'No Aplica'), ('VV', 'Verde vencido'), ('SA', 'Sin antecedentes')], max_length=2, null=True, verbose_name='Sello verde')),
                ('copropiedadInmobiliaria', models.BooleanField(blank=True, null=True, verbose_name='Copropiedad Inmobiliaria')),
                ('ocupante', models.CharField(blank=True, choices=[('P', 'Propietario'), ('A', 'Arrendatario'), ('O', 'Otro'), ('SO', 'Sin ocupante')], max_length=2, null=True, verbose_name='Ocupante')),
                ('tipoBien', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tipo de bien')),
                ('destinoSII', models.CharField(blank=True, choices=[('H', 'Habitacional'), ('O', 'Oficina'), ('C', 'Comercio'), ('I', 'Industria'), ('L', 'Bodega'), ('Z', 'Estacionamiento'), ('D', 'Deportes y Recreación'), ('E', 'Educación y Cultura'), ('G', 'Hotel, Motel'), ('P', 'Administración pública'), ('Q', 'Culto'), ('S', 'Salud')], max_length=1, null=True, verbose_name='Destino según SII')),
                ('usoActual', models.CharField(blank=True, max_length=20, null=True, verbose_name='Uso actual')),
                ('usoFuturo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Uso futuro')),
                ('permisoEdificacion', models.IntegerField(blank=True, null=True, verbose_name='Permiso edificación')),
                ('permisoEdificacionDate', models.DateField(blank=True, null=True, verbose_name='Permiso edificación fecha')),
                ('recepcionFinal', models.IntegerField(blank=True, null=True, verbose_name='Recepcion final')),
                ('recepcionFinalDate', models.DateField(blank=True, null=True, verbose_name='Recepcion final fecha')),
                ('expropiacion', models.BooleanField(blank=True, null=True, verbose_name='Expropiacion')),
                ('viviendaSocial', models.BooleanField(blank=True, null=True, verbose_name='Vivienda social')),
            ],
            bases=('realestate.realestate',),
        ),
    ]
