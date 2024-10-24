# Generated by Django 5.0.7 on 2024-10-24 10:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0014_apps_entidade_ticket_app_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 24, 10, 3, 53, 977174, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 24, 10, 3, 53, 974177, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 24, 10, 3, 53, 975175, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('Interno', 'Interno'), ('Operador', 'Operador'), ('Cliente', 'Cliente')], max_length=50, verbose_name='Cargo'),
        ),
    ]