# Generated by Django 2.0.7 on 2018-07-07 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('when_the_light_go_down', '0004_fiche_validation'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiche',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='wtlgd/perso'),
        ),
    ]
