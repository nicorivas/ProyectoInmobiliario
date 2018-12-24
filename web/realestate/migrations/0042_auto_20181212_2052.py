# Generated by Django 2.1 on 2018-12-12 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0041_auto_20181211_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='propertyType',
            field=models.PositiveIntegerField(choices=[('', '---------'), (1, 'Casa'), (2, 'Departamento'), (3, 'Edificio'), (4, 'Condominio'), (0, 'Otro')], default=0),
        ),
    ]