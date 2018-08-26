# Generated by Django 2.1 on 2018-08-17 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0002_auto_20180817_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='bathrooms',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Baños'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='bedrooms',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Dormitorios'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='orientation',
            field=models.CharField(blank=True, choices=[('N', 'Norte'), ('NE', 'Norponiente'), ('E', 'Poniente'), ('SE', 'Surponiente'), ('S', 'Sur'), ('WS', 'Suroriente'), ('W', 'Oriente'), ('NW', 'Nororiente')], max_length=2, null=True, verbose_name='Orientacion'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='totalSquareMeters',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='usefulSquareMeters',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Superficie util'),
        ),
    ]
