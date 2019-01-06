# Generated by Django 2.1 on 2019-01-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terrain', '0002_auto_20190105_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terrain',
            name='area',
            field=models.FloatField(blank=True, null=True, verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='terrain',
            name='uf_per_area',
            field=models.FloatField(blank=True, null=True, verbose_name='UF per Area'),
        ),
    ]
