# Generated by Django 2.1 on 2019-01-26 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0014_auto_20190126_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='property_main',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appraisals_main', to='appraisal.AppProperty'),
        ),
    ]
