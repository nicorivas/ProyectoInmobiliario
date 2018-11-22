# Generated by Django 2.1 on 2018-11-21 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0037_auto_20181119_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Rol')),
                ('state', models.IntegerField(blank=True, choices=[(0, 'Sin datos'), (1, 'Definitivo'), (2, 'Matriz'), (3, 'En trámite'), (4, 'Preasignado'), (5, 'Bien común'), (6, 'Uso y Goce'), (7, 'No enrolado')], default=0, verbose_name='Estado')),
            ],
        ),
        migrations.RemoveField(
            model_name='appraisal',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='appraisal',
            name='rolType',
        ),
        migrations.RemoveField(
            model_name='appraisalevaluation',
            name='id',
        ),
        migrations.AlterField(
            model_name='appraisalevaluation',
            name='appraisal',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='appraisal.Appraisal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appraisal',
            name='roles',
            field=models.ManyToManyField(to='appraisal.Rol'),
        ),
    ]