# Generated by Django 2.1 on 2018-12-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0015_auto_20181212_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='realestate_ptr',
        ),
    ]