# Generated by Django 2.1 on 2018-08-24 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('province', '0002_auto_20180824_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='province',
            name='code',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='Code'),
        ),
    ]