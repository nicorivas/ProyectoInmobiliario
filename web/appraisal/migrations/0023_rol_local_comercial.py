# Generated by Django 2.1 on 2019-02-09 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
        ('appraisal', '0022_auto_20190209_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='rol',
            name='local_comercial',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='store.Store'),
        ),
    ]
