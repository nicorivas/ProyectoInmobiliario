# Generated by Django 2.1 on 2018-09-13 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0011_auto_20180913_1549'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appraisal',
            options={'permissions': (('assign_tasador', 'Can assign tasadores'),)},
        ),
    ]
