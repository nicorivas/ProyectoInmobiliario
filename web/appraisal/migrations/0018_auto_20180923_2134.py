# Generated by Django 2.1 on 2018-09-24 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0017_auto_20180923_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='status',
            field=models.CharField(choices=[(1, 'active'), (2, 'finished')], default='a', max_length=10, verbose_name='Estado'),
        ),
    ]
