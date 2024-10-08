# Generated by Django 5.0.7 on 2024-10-08 11:38

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0021_alter_statuslog_datahora_alter_ticket_datacriacao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 8, 11, 38, 0, 867739, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 8, 11, 38, 0, 867739, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('Operador', 'Operador'), ('Interno', 'Interno'), ('Cliente', 'Cliente')], max_length=50, verbose_name='Cargo'),
        ),
        migrations.CreateModel(
            name='Entidades_Apps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.apps', verbose_name='Aplicação')),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.entidades', verbose_name='Utilizador')),
            ],
        ),
    ]