# Generated by Django 2.1 on 2018-12-13 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentBuilding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hola', models.BooleanField(default=False, verbose_name='Creado desde departamento')),
            ],
        ),
    ]