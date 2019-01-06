# Generated by Django 2.1 on 2019-01-05 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('apartment', '__first__'),
        ('realestate', '0001_initial'),
        ('apartmentbuilding', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('terrain', '0001_initial'),
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_type', models.PositiveIntegerField()),
                ('property_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Appraisal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeRequest', models.DateTimeField(blank=True, null=True, verbose_name='Time created')),
                ('timeDue', models.DateTimeField(blank=True, null=True, verbose_name='Time due')),
                ('timeCreated', models.DateTimeField(blank=True, null=True, verbose_name='Time created')),
                ('timeModified', models.DateTimeField(blank=True, null=True, verbose_name='Time modified')),
                ('timeFinished', models.DateTimeField(blank=True, null=True, verbose_name='Time finished')),
                ('timePaused', models.DateTimeField(blank=True, null=True, verbose_name='Time paused')),
                ('state', models.IntegerField(choices=[(4, 'not assigned'), (1, 'active'), (3, 'finished'), (2, 'paused'), (0, 'imported')], default=1, verbose_name='Estado')),
                ('source', models.IntegerField(blank=True, choices=[(1, 'Tasación'), (2, 'Portal Inmbiliario'), (3, 'TocToc')], default=1, null=True, verbose_name='Fuente de tasación')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Precio tasación')),
                ('visita', models.IntegerField(blank=True, choices=[('', '---------'), (0, 'Sin Visita'), (1, 'Completa'), (2, 'Solo Exterior')], null=True, verbose_name='Visita')),
                ('tipoTasacion', models.IntegerField(blank=True, choices=[('', '---------'), (1, 'Hipotecaria'), (7, 'Comercial'), (5, 'Terreno'), (6, 'Avance de obra'), (2, 'Revisión'), (3, 'Escritorio'), (4, 'Piloto'), (0, 'Otra')], null=True, verbose_name='Tipo Pedido')),
                ('finalidad', models.IntegerField(blank=True, choices=[('', '---------'), (2, 'Crédito'), (1, 'Garantía General'), (4, 'Venta Activos'), (6, 'Dación en Pago'), (3, 'Remate'), (5, 'Liquidación'), (7, 'Toma de Seguro'), (0, 'Otra')], null=True, verbose_name='Finalidad')),
                ('solicitante', models.IntegerField(blank=True, choices=[('', '---------'), (1, 'BCI'), (2, 'Santander'), (3, 'Itaú'), (4, 'Banco Internacional'), (5, 'Banco de Chile'), (6, 'Corpbanca'), (7, 'Scotiabank'), (8, 'BICE'), (0, 'Otro')], null=True, verbose_name='Solicitante')),
                ('solicitanteOtro', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante')),
                ('solicitanteSucursal', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante sucursal')),
                ('solicitanteCodigo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante código')),
                ('solicitanteEjecutivo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante ejecutivo')),
                ('solicitanteEjecutivoEmail', models.CharField(blank=True, max_length=100, null=True, verbose_name='Solicitante email')),
                ('solicitanteEjecutivoTelefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='Solicitante teléfono')),
                ('cliente', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cliente')),
                ('clienteRut', models.CharField(blank=True, max_length=13, null=True, verbose_name='Cliente RUT')),
                ('clienteEmail', models.CharField(blank=True, max_length=100, null=True, verbose_name='Cliente Email')),
                ('clienteTelefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='Cliente Teléfono')),
                ('contacto', models.CharField(blank=True, max_length=100, null=True, verbose_name='Contacto')),
                ('contactoRut', models.CharField(blank=True, max_length=13, null=True, verbose_name='Contacto RUT')),
                ('contactoEmail', models.CharField(blank=True, max_length=100, null=True, verbose_name='Contacto Email')),
                ('contactoTelefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='Contacto Teléfono')),
                ('propietario', models.CharField(blank=True, max_length=100, null=True, verbose_name='Propietario')),
                ('propietarioRut', models.CharField(blank=True, max_length=13, null=True, verbose_name='Propietario RUT')),
                ('propietarioEmail', models.CharField(blank=True, max_length=100, null=True, verbose_name='Contacto Email')),
                ('propietarioTelefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='Contacto Teléfono')),
                ('propietarioReferenceSII', models.BooleanField(blank=True, default=False, verbose_name='Propietario Referencia SII')),
                ('visadorEmpresa', models.CharField(blank=True, max_length=100, null=True, verbose_name='Visador empresa')),
                ('visadorEmpresaMail', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Visador empresa mail')),
                ('orderFile', models.FileField(blank=True, null=True, upload_to='orders/', verbose_name='Documento pedido')),
                ('commentsOrder', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Comentarios pedido')),
                ('descripcionSector', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripción sector')),
                ('descripcionPlanoRegulador', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripción plano regulador')),
                ('descripcionExpropiacion', models.TextField(blank=True, default='', max_length=10000, null=True, verbose_name='Descripción expropiación')),
                ('valorUF', models.FloatField(blank=True, null=True, verbose_name='Valor UF')),
            ],
            options={
                'permissions': (('assign_tasador', 'Can assign tasadores'), ('assign_visador', 'Can assign visadores')),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.IntegerField(choices=[(1, 'Contacto validado'), (9, 'Cliente validado'), (23, 'Tasador solicitado'), (2, 'Solicitud de tasador aceptada'), (6, 'Solicitud de tasador rechazada'), (25, 'Tasador desasignado'), (26, 'Visador asignado'), (27, 'Visador desasignado'), (24, 'Tasación ingresada'), (3, 'Visita acordada'), (4, 'Propiedad visitada'), (5, 'Enviado a visador'), (8, 'Entregado al cliente'), (10, 'Contabilización'), (18, 'Abortado'), (19, 'Incidencia'), (20, 'Corrección informe'), (21, 'Observación visador'), (22, 'Objeción'), (0, 'Otro')], default=0)),
                ('text', models.CharField(max_length=500, verbose_name='Comment')),
                ('conflict', models.BooleanField(default=False, verbose_name='Incidencia')),
                ('timeCreated', models.DateTimeField(blank=True, null=True, verbose_name='Time created')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ImageField(default='no-img.jpg', upload_to='test/')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(default='no-img.jpg', upload_to='test/')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=20, null=True, verbose_name='Rol')),
                ('state', models.IntegerField(blank=True, choices=[(0, 'Sin datos'), (1, 'Definitivo'), (2, 'Matriz'), (3, 'En trámite'), (4, 'Preasignado'), (5, 'Bien común'), (6, 'Uso y Goce'), (7, 'No enrolado')], default=0, verbose_name='Estado')),
                ('apartment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='apartment.Apartment')),
                ('apartment_building', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='apartmentbuilding.ApartmentBuilding')),
                ('house', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='house.House')),
                ('terrain', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='terrain.Terrain')),
            ],
        ),
        migrations.CreateModel(
            name='AppraisalEvaluation',
            fields=[
                ('appraisal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='appraisal.Appraisal')),
                ('completeness', models.BooleanField(blank=True, default=True, verbose_name='Aceptación del informe completo (50%)')),
                ('onTime', models.BooleanField(blank=True, default=True, verbose_name='Entrega a tiempo (25%)')),
                ('correctSurface', models.BooleanField(blank=True, default=True, verbose_name='Superficies correctas -hasta un 5% de error- (15%)')),
                ('completeNormative', models.BooleanField(blank=True, default=True, verbose_name='Normativa Completa y correcta (5%)')),
                ('homologatedReferences', models.BooleanField(blank=True, default=True, verbose_name='Referencias Homologables si las hubieran (2,5%)')),
                ('generalQuality', models.BooleanField(blank=True, default=True, verbose_name='Calidad General -peso, imagenes claras configuración- (2,5%)')),
                ('commentText', models.CharField(blank=True, max_length=500, verbose_name='Comentarios de la tasación')),
                ('commentFeedback', models.CharField(blank=True, max_length=500, verbose_name='Feedback de la tasación')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appraisal',
            name='comments',
            field=models.ManyToManyField(to='appraisal.Comment'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='documents',
            field=models.ManyToManyField(to='appraisal.Document'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='photos',
            field=models.ManyToManyField(to='appraisal.Photo'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='real_estates',
            field=models.ManyToManyField(to='realestate.RealEstate'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='roles',
            field=models.ManyToManyField(to='appraisal.Rol'),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='tasadorUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appraisals_tasador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appraisal',
            name='visadorUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appraisals_visador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appproperty',
            name='appraisal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appraisal.Appraisal'),
        ),
    ]
