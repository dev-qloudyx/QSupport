# Generated by Django 4.2.3 on 2024-09-20 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0005_alter_usuarios_foto_alter_usuarios_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='role',
            field=models.CharField(choices=[('CLIENTE', 'Cliente'), ('QLOUDYX', 'Qloudyx'), ('OPERADOR', 'Operador')], max_length=50),
        ),
    ]
