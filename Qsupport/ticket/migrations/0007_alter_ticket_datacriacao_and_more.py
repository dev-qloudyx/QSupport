# Generated by Django 4.2.3 on 2024-09-23 10:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_alter_usuarios_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='dataCriacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 23, 10, 31, 53, 840981, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='id_Proprietario',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='prioridade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.prioridade'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='resolucao',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.resolucao'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='usuarios',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('OPERADOR', 'Operador'), ('QLOUDYX', 'Qloudyx'), ('CLIENTE', 'Cliente')], max_length=50),
        ),
    ]
