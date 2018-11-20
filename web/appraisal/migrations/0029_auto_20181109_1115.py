# Generated by Django 2.1 on 2018-11-09 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0028_appraisal_valuationrealestate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='rolAvaluo',
        ),
        migrations.AddField(
            model_name='appraisal',
            name='rol',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Rol'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='rolType',
            field=models.IntegerField(blank=True, choices=[(0, 'Sin datos'), (1, 'Definitivo'), (2, 'Matriz'), (3, 'En trámite'), (4, 'Preasignado'), (5, 'Bien común'), (6, 'Uso y Goce'), (7, 'No enrolado')], default=0, verbose_name='Tipo rol'),
        ),
    ]