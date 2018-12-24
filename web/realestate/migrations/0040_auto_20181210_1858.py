# Generated by Django 2.1 on 2018-12-10 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0039_auto_20181210_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestate',
            name='propertyType',
            field=models.PositiveIntegerField(choices=[('', '---------'), (1, 'Casa'), (2, 'Departamento'), (3, 'Edificio'), (4, 'Condominio'), (0, 'Otro')], default=0),
        ),
    ]