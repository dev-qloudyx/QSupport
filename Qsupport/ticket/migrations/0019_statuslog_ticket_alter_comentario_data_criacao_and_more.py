# Generated by Django 4.2.3 on 2024-10-29 15:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0018_alter_comentario_data_criacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='statuslog',
            name='ticket',
            field=models.ForeignKey(default=23, on_delete=django.db.models.deletion.CASCADE, to='ticket.ticket', verbose_name='Ticket'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comentario',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 15, 26, 24, 152379, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 15, 26, 24, 151378, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 29, 15, 26, 24, 151378, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('Cliente', 'Cliente'), ('Operador', 'Operador'), ('Interno', 'Interno')], max_length=50, verbose_name='Cargo'),
        ),
    ]
