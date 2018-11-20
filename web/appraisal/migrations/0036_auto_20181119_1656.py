# Generated by Django 2.1 on 2018-11-19 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0035_auto_20181119_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='descripcionExpropiacion',
            field=models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripción expropiación'),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='descripcionPlanoRegulador',
            field=models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripción plano regulador'),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='descripcionSector',
            field=models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripción sector'),
        ),
    ]