# Generated by Django 2.0.6 on 2018-06-29 10:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('magasin', '0010_auto_20180629_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 29, 10, 5, 46, 431845, tzinfo=utc)),
        ),
    ]
