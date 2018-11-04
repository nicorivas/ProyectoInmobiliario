# Generated by Django 2.1 on 2018-11-01 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0024_appraisal_visita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='solicitante',
            field=models.CharField(blank=True, choices=[(1, 'BCI'), (2, 'Santander'), (3, 'Itaú'), (4, 'Banco Internacional'), (5, 'Banco de Chile'), (6, 'Corpbanca'), (7, 'Scotiabank'), (8, 'BICE'), (0, 'Otro')], max_length=100, null=True, verbose_name='Solicitante'),
        ),
    ]