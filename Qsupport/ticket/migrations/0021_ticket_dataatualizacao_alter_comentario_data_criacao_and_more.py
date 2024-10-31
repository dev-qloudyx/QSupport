# Generated by Django 4.2.3 on 2024-10-31 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0020_ticket_url_alter_comentario_data_criacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='dataAtualizacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 16, 37, 25, 969756, tzinfo=datetime.timezone.utc), null=True, verbose_name='Atualizado a'),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='data_criacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 16, 37, 25, 971756, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='dataHora',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 16, 37, 25, 970756, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 31, 16, 37, 25, 969756, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('Interno', 'Interno'), ('Operador', 'Operador'), ('Cliente', 'Cliente')], max_length=50, verbose_name='Cargo'),
        ),
    ]
