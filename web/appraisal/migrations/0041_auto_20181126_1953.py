# Generated by Django 2.1 on 2018-11-26 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0040_auto_20181123_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='contactoRut',
            field=models.CharField(blank=True, max_length=13, null=True, verbose_name='Contacto RUT'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='propietarioEmail',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Contacto Email'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='propietarioTelefono',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Contacto Teléfono'),
        ),
    ]