# Generated by Django 2.1 on 2018-11-09 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0017_remove_realestate_dfl2'),
    ]

    operations = [
        migrations.AddField(
            model_name='realestate',
            name='dfl2',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'S/A'), (2, 'Si'), (3, 'No')], default=1, verbose_name='DFL 2'),
        ),
    ]