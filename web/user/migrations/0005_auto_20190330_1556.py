# Generated by Django 2.1 on 2019-03-30 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190327_1946'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('view_accounting', 'Can view accounting'), ('evaluate_tasador', 'Can evaluate appraisers'))},
        ),
    ]