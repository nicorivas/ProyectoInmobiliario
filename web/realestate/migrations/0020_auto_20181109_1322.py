# Generated by Django 2.1 on 2018-11-09 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0019_auto_20181109_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='adobe',
            field=models.BooleanField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Adobe'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='copropiedadInmobiliaria',
            field=models.BooleanField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Copropiedad Inmobiliaria'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='desmontable',
            field=models.BooleanField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Desmontable'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='expropiacion',
            field=models.BooleanField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Expropiacion'),
        ),
        migrations.AddField(
            model_name='realestate',
            name='viviendaSocial',
            field=models.BooleanField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='Vivienda social'),
        ),
    ]
