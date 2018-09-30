<<<<<<< HEAD
# Generated by Django 2.1.1 on 2018-09-29 21:16
=======
# Generated by Django 2.1 on 2018-09-30 12:37
>>>>>>> 24e7adb57ec744c86e5a6ec44accc51d350a96d5

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propertyType', models.PositiveIntegerField(choices=[(0, 'Indefinido'), (1, 'Casa'), (2, 'Departamento'), (3, 'Edificio')], default=0)),
                ('timeCreated', models.DateTimeField(blank=True, null=True, verbose_name='Time created')),
                ('timeModified', models.DateTimeField(blank=True, null=True, verbose_name='Time modified')),
                ('timeFinished', models.DateTimeField(blank=True, null=True, verbose_name='Time finished')),
                ('timeDue', models.DateTimeField(blank=True, null=True, verbose_name='Time due')),
                ('status', models.IntegerField(choices=[(1, 'active'), (2, 'finished')], default=1, verbose_name='Estado')),
                ('solicitante', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante')),
                ('solicitanteSucursal', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante sucursal')),
                ('solicitanteEjecutivo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante ejecutivo')),
                ('cliente', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cliente')),
                ('clienteRut', models.IntegerField(blank=True, null=True, verbose_name='Cliente RUT')),
                ('propietario', models.CharField(blank=True, max_length=100, null=True, verbose_name='Propietario')),
                ('propietarioRut', models.IntegerField(blank=True, null=True, verbose_name='Propietario RUT')),
                ('rolAvaluo', models.IntegerField(blank=True, null=True, verbose_name='Rol principal')),
                ('visadorEmpresa', models.CharField(blank=True, max_length=100, null=True, verbose_name='Visador empresa')),
                ('visadorEmpresaMail', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Visador empresa mail')),
                ('valorUF', models.IntegerField(blank=True, null=True, verbose_name='Valor UF')),
            ],
            options={
                'permissions': (('assign_tasador', 'Can assign tasadores'), ('assign_visador', 'Can assign visadores')),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500, verbose_name='Comment')),
                ('timeCreated', models.DateTimeField(blank=True, null=True, verbose_name='Time created')),
                ('appraisal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appraisal.Appraisal')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
