# Generated by Django 2.1 on 2018-09-25 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0002_auto_20180924_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='timeDue',
        ),
    ]
