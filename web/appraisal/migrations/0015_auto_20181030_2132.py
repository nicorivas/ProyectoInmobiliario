# Generated by Django 2.1 on 2018-10-31 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0014_auto_20181030_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='propietarioRut',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Propietario RUT'),
        ),
    ]
