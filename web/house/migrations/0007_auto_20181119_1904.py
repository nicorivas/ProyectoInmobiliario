# Generated by Django 2.1 on 2018-11-19 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0006_house_addressnumber2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='addressNumber2',
            field=models.TextField(blank=True, max_length=30, null=True, verbose_name='Lote'),
        ),
    ]