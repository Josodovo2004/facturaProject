# Generated by Django 5.1 on 2024-08-12 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0004_tipoprecio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tipoPrecio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacion.tipoprecio'),
        ),
    ]
