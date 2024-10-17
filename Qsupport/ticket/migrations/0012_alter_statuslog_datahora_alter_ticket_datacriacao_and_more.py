# Generated by Django 4.2.3 on 2024-10-14 14:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0011_alter_statuslog_datahora_alter_ticket_datacriacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 14, 14, 40, 31, 755964, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 14, 14, 40, 31, 755964, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('Operador', 'Operador'), ('Interno', 'Interno'), ('Cliente', 'Cliente')], max_length=50, verbose_name='Cargo'),
        ),
    ]