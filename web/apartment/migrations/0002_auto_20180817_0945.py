# Generated by Django 2.1 on 2018-08-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='floor',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Piso'),
        ),
    ]