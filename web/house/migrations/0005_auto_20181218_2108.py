# Generated by Django 2.1 on 2018-12-19 00:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('building', '0015_auto_20181218_1845'),
        ('appraisal', '0051_auto_20181218_1828'),
        ('house', '0004_auto_20181218_2056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='realestate_ptr',
        ),
        migrations.DeleteModel(
            name='House',
        ),
    ]
