# Generated by Django 2.1 on 2019-05-08 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0027_auto_20190325_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='tipoTasacion',
            field=models.IntegerField(blank=True, choices=[('', '---------'), (1, 'Hipotecaria'), (8, 'Garantía general'), (9, 'Pre-informe'), (11, 'Evaluación proyecto inmobiliario'), (12, 'Evaluación proyecto autoconstrucción'), (6, 'Avance de obra inmobiliario'), (10, 'Avance de obra autoconstrucción'), (20, 'Retasación garantía general'), (13, 'Final inmobiliaria'), (14, 'Final autoconstrucción'), (15, 'Remate'), (16, 'Agrícola'), (17, 'Vehículo'), (18, 'Máquinas y equipos'), (2, 'Revisión'), (19, 'Leasing'), (0, 'Otro')], null=True, verbose_name='Tipo Pedido'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='event',
            field=models.IntegerField(choices=[(1, 'Contacto validado'), (30, 'Contacto invalidado'), (9, 'Cliente validado'), (29, 'Cliente invalido'), (18, 'Tasación anulada'), (23, 'Tasador solicitado'), (2, 'Solicitud de tasador aceptada'), (6, 'Solicitud de tasador rechazada'), (25, 'Tasador desasignado'), (26, 'Visador asignado'), (27, 'Visador desasignado'), (24, 'Tasación ingresada'), (3, 'Visita acordada'), (4, 'Propiedad visitada'), (5, 'Enviado a visador'), (31, 'Devuelta a tasador'), (32, 'Devuelta a visador'), (8, 'Entregado al cliente'), (10, 'Contabilización'), (19, 'Incidencia'), (20, 'Corrección informe'), (21, 'Observación visador'), (33, 'Reporte adjunto'), (28, 'Comentario'), (34, 'Tasación devuelta por cliente'), (0, 'Otro')], default=0),
        ),
    ]
