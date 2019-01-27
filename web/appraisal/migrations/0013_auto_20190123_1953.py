# Generated by Django 2.1 on 2019-01-23 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0012_auto_20190117_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='event',
            field=models.IntegerField(choices=[(1, 'Contacto validado'), (9, 'Cliente validado'), (23, 'Tasador solicitado'), (2, 'Solicitud de tasador aceptada'), (6, 'Solicitud de tasador rechazada'), (25, 'Tasador desasignado'), (26, 'Visador asignado'), (27, 'Visador desasignado'), (24, 'Tasación ingresada'), (3, 'Visita acordada'), (4, 'Propiedad visitada'), (5, 'Enviado a visador'), (8, 'Entregado al cliente'), (10, 'Contabilización'), (19, 'Incidencia'), (20, 'Corrección informe'), (21, 'Observación visador'), (28, 'Comentario'), (0, 'Otro')], default=0),
        ),
    ]
