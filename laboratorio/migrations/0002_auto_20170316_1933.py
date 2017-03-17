# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 00:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratorio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=200)),
                ('valorUnitario', models.IntegerField()),
                ('unidadesExistentes', models.IntegerField()),
                ('clasificacion', models.CharField(choices=[('MaterialesVivos', (('Bac', 'Bacterias'), ('Hon', 'Hongos'))), ('MediosDeCultivo', (('Glu', 'Glucosa'), ('Fru', 'Fructuosa'), ('Tri', 'Triptona'), ('Pep', 'Peptona'))), ('Micronutrientes', (('Fe', 'Hierro'), ('Mg', 'Magnesio'), ('P', 'Fosforo'))), ('ManipulacionADNYProteinas', (('Pri', 'Primers'), ('Kem', 'Kits de extraccion metagenomica'), ('KeADN', 'Kits de extraccion ADN aislado'), ('Pup', 'Purificador de proteinas'), ('Enr', 'Enzimas de restriccion'), ('Pro', 'Proteasas'))), ('Otros', 'Moleculas genericas')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TipoBodega',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='bodega',
            name='cupo_bandeja',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bodega',
            name='estado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bodega',
            name='fecha_actualizacion',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='bodega',
            name='fecha_creacion',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 16, 19, 33, 44, 454000)),
        ),
        migrations.AddField(
            model_name='bodega',
            name='numero_bandejas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bodega',
            name='serial',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='bodega',
            name='temperatura_media',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
        migrations.AddField(
            model_name='bodega',
            name='temperatura_minima',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
        migrations.AddField(
            model_name='bodega',
            name='usuario_actualizacion',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bodega',
            name='usuario_creacion',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bodega',
            name='limite',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bodega',
            name='tipo_bodega',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratorio.TipoBodega'),
        ),
    ]