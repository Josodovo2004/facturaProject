# Generated by Django 5.1 on 2024-08-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0009_rename_name_catalogo05tipostributos_nombre_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TipoComprobante',
        ),
        migrations.AddField(
            model_name='catalogo05tipostributos',
            name='un_ece_5305',
            field=models.CharField(blank=True, db_column='UN_ECE_5305', max_length=1, null=True),
        ),
    ]
