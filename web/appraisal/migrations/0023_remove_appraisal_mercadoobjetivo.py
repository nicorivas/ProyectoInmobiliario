# Generated by Django 2.1 on 2018-11-01 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0022_auto_20181101_1528'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='mercadoObjetivo',
        ),
    ]