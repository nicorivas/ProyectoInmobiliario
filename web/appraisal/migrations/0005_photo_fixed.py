# Generated by Django 2.1 on 2019-01-07 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0004_comment_appraisal'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='fixed',
            field=models.BooleanField(default=False, verbose_name='Fixed'),
        ),
    ]
