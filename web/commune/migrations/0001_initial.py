# Generated by Django 2.1 on 2019-05-13 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('province', '0001_initial'),
        ('region', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('name_simple', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre simple')),
                ('code', models.PositiveSmallIntegerField(unique=True, verbose_name='Code')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='province.Province', to_field='code', verbose_name='Provincia')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.Region', to_field='code', verbose_name='Region')),
            ],
        ),
        migrations.CreateModel(
            name='CommuneFull',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('name_simple', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre simple')),
                ('code', models.PositiveSmallIntegerField(unique=True, verbose_name='Code')),
                ('dataApartmentCount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Departamentos')),
                ('dataHouseCount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Casas')),
                ('dataBuildingCount', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Edificios')),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='province.ProvinceFull', to_field='code', verbose_name='Provincia')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='region.RegionFull', to_field='code', verbose_name='Region')),
            ],
        ),
    ]
