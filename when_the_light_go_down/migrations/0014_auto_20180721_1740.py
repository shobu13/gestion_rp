# Generated by Django 2.0.7 on 2018-07-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('when_the_light_go_down', '0013_auto_20180721_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiche',
            name='photo',
            field=models.ImageField(blank=True, default='img/054.jpg', null=True, upload_to='wtlgd/perso'),
        ),
    ]
