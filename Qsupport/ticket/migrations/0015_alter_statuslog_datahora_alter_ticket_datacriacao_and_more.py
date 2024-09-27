# Generated by Django 5.0.7 on 2024-09-27 14:11

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0014_alter_statuslog_datahora_alter_ticket_datacriacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 27, 14, 11, 29, 266587, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 27, 14, 11, 29, 266587, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='usuario_app',
            field=models.ForeignKey(limit_choices_to={'usuario': 'TesteUser'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.usuarios_apps'),
        ),
    ]
