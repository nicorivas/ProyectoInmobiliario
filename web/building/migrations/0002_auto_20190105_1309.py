# Generated by Django 2.1 on 2019-01-05 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='area',
            field=models.FloatField(blank=True, null=True, verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='building',
            name='UFPerArea',
            field=models.FloatField(blank=True, default=0, verbose_name='Area density'),
        ),
    ]