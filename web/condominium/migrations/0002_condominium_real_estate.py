# Generated by Django 2.1 on 2019-05-13 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0002_price_appraisal'),
        ('condominium', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominium',
            name='real_estate',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='realestate.RealEstate', verbose_name='Real estate'),
            preserve_default=False,
        ),
    ]