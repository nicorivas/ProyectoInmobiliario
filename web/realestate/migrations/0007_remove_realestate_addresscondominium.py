# Generated by Django 2.1 on 2019-05-17 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0006_auto_20190517_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='realestate',
            name='addressCondominium',
        ),
    ]
