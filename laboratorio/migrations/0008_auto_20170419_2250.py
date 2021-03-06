# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 03:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0007_detalleorden_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad_media_uso',
            field=models.DecimalField(decimal_places=8, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='frecuencia_media_uso',
            field=models.CharField(choices=[('Continua', 'Muchas veces al dia'), ('Frecuente', 'Al menos 1 vez al dia'), ('Ocasional', 'Al menos 1 vez a la semana'), ('PocoUsual', 'Al menos 1 vez al mes'), ('Rara', 'Unas pocas veces al anio'), ('MuyRara', 'Al menos 1 vez al anio'), ('NA', 'NA')], max_length=26, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='frecuencia_minima_uso',
            field=models.CharField(choices=[('Continua', 'Muchas veces al dia'), ('Frecuente', 'Al menos 1 vez al dia'), ('Ocasional', 'Al menos 1 vez a la semana'), ('PocoUsual', 'Al menos 1 vez al mes'), ('Rara', 'Unas pocas veces al anio'), ('MuyRara', 'Al menos 1 vez al anio'), ('NA', 'NA')], max_length=26, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='punto_pedido',
            field=models.DecimalField(decimal_places=8, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='stock_seguridad',
            field=models.DecimalField(decimal_places=8, max_digits=15, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='tiempo_reaprovisionamiento',
            field=models.IntegerField(default=0),
        ),
    ]
