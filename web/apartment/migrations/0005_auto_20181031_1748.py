# Generated by Django 2.1 on 2018-10-31 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0004_auto_20181018_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='permisoEdificacionNo',
            field=models.CharField(default=0, max_length=20, null=True, verbose_name='Numero permiso edificacion'),
        ),
    ]
