# Generated by Django 2.1 on 2018-12-13 02:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0049_appraisal_commentsorder'),
        ('building', '0009_auto_20181101_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='realestate_ptr',
        ),
        migrations.DeleteModel(
            name='Building',
        ),
    ]
