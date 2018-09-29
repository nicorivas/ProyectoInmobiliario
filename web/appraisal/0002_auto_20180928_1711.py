# Generated by Django 2.1.1 on 2018-09-28 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0009_auto_20180925_2213'),
        ('appraisal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='house.House', verbose_name='Casa'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='propertyType',
            field=models.PositiveIntegerField(choices=[(0, 'Indefinido'), (1, 'Casa'), (2, 'Departamento'), (3, 'Edificio')], default=0),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='apartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apartment.Apartment', verbose_name='Departamento'),
        ),
    ]
