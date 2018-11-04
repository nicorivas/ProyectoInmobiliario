# Generated by Django 2.1 on 2018-11-01 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0006_apartment_mercadoobjetivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='mercadoObjetivo',
            field=models.BooleanField(blank=True, choices=[(None, 'S/A'), (True, 'Si'), (False, 'No')], null=True, verbose_name='Mercado objetivo'),
        ),
    ]