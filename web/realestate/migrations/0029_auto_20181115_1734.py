# Generated by Django 2.1 on 2018-11-15 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0028_realestate_sourceaddedmanually'),
    ]

    operations = [
        migrations.AddField(
            model_name='terrain',
            name='fondo',
            field=models.FloatField(blank=True, null=True, verbose_name='Fondo'),
        ),
        migrations.AddField(
            model_name='terrain',
            name='frente',
            field=models.FloatField(blank=True, null=True, verbose_name='Frente'),
        ),
        migrations.AddField(
            model_name='terrain',
            name='rol',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Rol'),
        ),
        migrations.AddField(
            model_name='terrain',
            name='shape',
            field=models.IntegerField(blank=True, choices=[(0, 'Plano'), (1, 'Pendiente'), (2, 'Pendiente abrupta')], null=True, verbose_name='Forma'),
        ),
        migrations.AddField(
            model_name='terrain',
            name='topography',
            field=models.IntegerField(blank=True, choices=[(0, 'Plano'), (1, 'Pendiente'), (2, 'Pendiente abrupta')], null=True, verbose_name='Topografía'),
        ),
    ]
