# Generated by Django 2.1 on 2019-05-13 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('condominium', '0002_condominium_real_estate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condominium',
            name='real_estate',
        ),
    ]
