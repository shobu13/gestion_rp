# Generated by Django 2.0.7 on 2018-07-20 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('when_the_light_go_down', '0009_auto_20180720_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuivrons', models.IntegerField(default=0)),
                ('argentions', models.IntegerField(default=0)),
                ('orions', models.IntegerField(default=0)),
                ('perso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='when_the_light_go_down.Fiche')),
            ],
        ),
        migrations.AlterField(
            model_name='inventaire',
            name='perso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='when_the_light_go_down.Fiche'),
        ),
    ]
