# Generated by Django 2.0.6 on 2018-06-27 09:05

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0007_auto_20180627_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='frais_port',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='magasin.FraisDePort'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commande',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 27, 9, 5, 36, 842502, tzinfo=utc)),
        ),
    ]
