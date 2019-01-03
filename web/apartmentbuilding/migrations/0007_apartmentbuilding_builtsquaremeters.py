# Generated by Django 2.1 on 2018-12-28 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartmentbuilding', '0006_apartmentbuilding_addressnumber2'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentbuilding',
            name='builtSquareMeters',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie construida'),
        ),
    ]