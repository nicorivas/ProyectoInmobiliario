# Generated by Django 2.1 on 2018-12-10 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0048_auto_20181210_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='commentsOrder',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Comentarios pedido'),
        ),
    ]