# Generated by Django 2.1 on 2018-12-19 00:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0007_remove_house_old_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='building',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='building.Building', verbose_name='Edificio'),
        ),
    ]
