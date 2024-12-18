# Generated by Django 4.2.3 on 2024-10-29 15:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0016_alter_comentario_data_criacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 15, 26, 0, 271470, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 15, 26, 0, 270473, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 15, 26, 0, 270473, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('Operador', 'Operador'), ('Cliente', 'Cliente'), ('Interno', 'Interno')], max_length=50, verbose_name='Cargo'),
        ),
    ]
