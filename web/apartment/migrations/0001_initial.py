from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('realestate', '0001_initial'),
        ('building', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('realestate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='realestate.RealEstate')),
                ('number', models.CharField(max_length=10, null=True, verbose_name='Numero')),
                ('floor', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Piso')),
                ('bedrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Dormitorios')),
                ('bathrooms', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Baños')),
                ('builtSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie construida')),
                ('usefulSquareMeters', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie util')),
                ('orientation', models.CharField(blank=True, choices=[('N', 'Norte'), ('NE', 'Norponiente'), ('E', 'Poniente'), ('SE', 'Surponiente'), ('S', 'Sur'), ('WS', 'Suroriente'), ('W', 'Oriente'), ('NW', 'Nororiente')], max_length=2, null=True, verbose_name='Orientacion')),
                ('generalDescription', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripcion general')),
                ('tipoPropiedad', models.PositiveSmallIntegerField(choices=[(0, 'Usada'), (1, 'Nueva')], default=0, null=True, verbose_name='Tipo de propiedad')),
                ('antiguedad', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Antiguedad')),
                ('vidaUtil', models.PositiveSmallIntegerField(default=80, null=True, verbose_name='Vida util')),
                ('selloDeGases', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='Sello de gases')),
                ('permisoEdificacionNo', models.PositiveSmallIntegerField(default=0, null=True, verbose_name='Numero permiso edificacion')),
                ('permisoEdificacionFecha', models.DateField(default='2006-10-25', null=True, verbose_name='Fecha permiso edificacion')),
                ('permisoEdificacionSuperficie', models.DecimalField(decimal_places=2, default=0, max_digits=7, null=True, verbose_name='Superficie permiso edificacion')),
                ('marketPrice', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Precio mercado UF')),
                ('sourceUrl', models.URLField(blank=True, null=True, verbose_name='Source url')),
                ('sourceName', models.CharField(blank=True, max_length=20, null=True, verbose_name='Source name')),
                ('sourceId', models.CharField(blank=True, max_length=20, null=True, verbose_name='Source id')),
                ('building_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='building.Building', verbose_name='Edificio')),
            ],
            bases=('realestate.realestate',),
        ),
    ]
