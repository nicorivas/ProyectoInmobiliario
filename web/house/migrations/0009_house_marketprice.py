# Generated by Django 2.1 on 2018-12-24 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0008_auto_20181218_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='marketPrice',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio mercado'),
        ),
    ]