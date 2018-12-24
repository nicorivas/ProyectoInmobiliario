# Generated by Django 2.1 on 2018-12-18 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0050_auto_20181214_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal',
            name='finalidad',
            field=models.IntegerField(blank=True, choices=[('', '---------'), (2, 'Crédito'), (1, 'Garantía General'), (4, 'Venta Activos'), (6, 'Dación en Pago'), (3, 'Remate'), (5, 'Liquidación'), (7, 'Toma de Seguro'), (0, 'Otra')], null=True, verbose_name='Finalidad'),
        ),
        migrations.AlterField(
            model_name='appraisal',
            name='tipoTasacion',
            field=models.IntegerField(blank=True, choices=[('', '---------'), (1, 'Hipotecaria'), (7, 'Comercial'), (5, 'Terreno'), (6, 'Avance de obra'), (2, 'Revisión'), (3, 'Escritorio'), (4, 'Piloto'), (0, 'Otra')], null=True, verbose_name='Tipo Pedido'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='event',
            field=models.IntegerField(choices=[(1, 'Contacto validado'), (2, 'Asignación aceptada'), (6, 'Asignación rechazada'), (9, 'Cliente validado'), (23, 'Tasador asignado'), (26, 'Visador asignado'), (25, 'Tasador desasignado'), (27, 'Visador desasignado'), (24, 'Tasación ingresada'), (3, 'Visita acordada'), (4, 'Propiedad visitada'), (5, 'Enviado a visador'), (8, 'Entregado al cliente'), (10, 'Contabilización'), (18, 'Abortado'), (19, 'Incidencia'), (20, 'Corrección informe'), (21, 'Observación visador'), (22, 'Objeción'), (0, 'Otro')], default=0),
        ),
    ]