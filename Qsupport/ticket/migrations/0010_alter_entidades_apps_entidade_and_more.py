# Generated by Django 4.2.3 on 2024-10-14 12:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0009_alter_statuslog_datahora_alter_ticket_datacriacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidades_apps',
            name='entidade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.entidades', verbose_name='Entidade'),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 14, 12, 17, 10, 562767, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 14, 12, 17, 10, 562767, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
    ]
