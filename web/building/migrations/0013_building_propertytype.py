# Generated by Django 2.1 on 2018-09-25 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0012_auto_20180904_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='propertyType',
            field=models.PositiveIntegerField(choices=[(0, 'Indefinido'), (1, 'Casa'), (2, 'Departamento'), (3, 'Edificio')], default=0),
        ),
    ]
