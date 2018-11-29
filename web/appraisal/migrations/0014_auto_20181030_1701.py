# Generated by Django 2.1.1 on 2018-10-30 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0013_auto_20181028_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='objetivo',
            field=models.CharField(blank=True, choices=[(0, 'Otro'), (1, 'Garantía'), (2, 'Crédito'), (3, 'Remate'), (4, 'Venta'), (5, 'Liquidación')], max_length=100, null=True, verbose_name='Objetivo'),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='source',
            field=models.IntegerField(blank=True, choices=[(1, 'Tasación'), (2, 'Portal Inmbiliario'), (3, 'TocToc')], default=1, null=True, verbose_name='Fuente de tasación'),
        ),
    ]