# Generated by Django 2.1 on 2018-10-12 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0003_auto_20181012_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='conflict',
            field=models.BooleanField(default=False, verbose_name='Incidencia'),
        ),
    ]
