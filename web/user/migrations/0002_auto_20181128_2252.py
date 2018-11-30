# Generated by Django 2.1 on 2018-11-29 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ntype', models.CharField(default='', max_length=100)),
                ('appraisal_id', models.IntegerField(null=True)),
                ('comment_id', models.IntegerField(null=True)),
                ('time_created', models.DateTimeField(blank=True, null=True, verbose_name='Time created')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='notifications',
            field=models.ManyToManyField(to='user.Notification'),
        ),
    ]
