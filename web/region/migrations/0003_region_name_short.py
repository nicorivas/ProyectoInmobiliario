# Generated by Django 2.1 on 2019-05-13 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('region', '0002_regionfull_name_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='name_short',
            field=models.CharField(default='', max_length=100, verbose_name='Nombre'),
            preserve_default=False,
        ),
    ]
