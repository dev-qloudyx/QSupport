# Generated by Django 4.2.3 on 2024-10-10 13:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100, unique=True, verbose_name='Utilizador')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='users/uploads/fotos', verbose_name='Foto')),
                ('descricao', models.CharField(max_length=250, null=True)),
                ('role', models.CharField(choices=[('Operador', 'Operador'), ('Cliente', 'Cliente'), ('Interno', 'Interno')], max_length=50, verbose_name='Cargo')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, unique=True, verbose_name='Telefone')),
                ('date_of_birth', models.DateField(verbose_name='Data de Nascimento')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo?')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin?')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Apps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Aplicação')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo?')),
            ],
        ),
        migrations.CreateModel(
            name='Apps_tpPedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apps', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.apps', verbose_name='Aplicação')),
            ],
        ),
        migrations.CreateModel(
            name='Entidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('externo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
                ('cor', models.CharField(max_length=30)),
                ('font_color', models.CharField(max_length=30)),
                ('descricao', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Prioridade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Tipo')),
                ('peso', models.CharField(max_length=50, verbose_name='Peso')),
            ],
        ),
        migrations.CreateModel(
            name='Resolucao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='StatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataHora', models.DateTimeField(default=datetime.datetime(2024, 10, 10, 13, 2, 41, 88821, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação')),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.estado', verbose_name='Estado')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='TiposPedidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Pedido')),
                ('descricao', models.CharField(max_length=300, verbose_name='Descrição')),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios_Apps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.apps', verbose_name='Aplicação')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilizador')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50, verbose_name='Titulo')),
                ('dataCriacao', models.DateTimeField(default=datetime.datetime(2024, 10, 10, 13, 2, 41, 89320, tzinfo=datetime.timezone.utc), verbose_name='Data de Criação')),
                ('descricao', models.CharField(max_length=300, verbose_name='Descrição')),
                ('app_tpPedidos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.apps_tppedidos', verbose_name='Tipo de Problema')),
                ('estado', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.statuslog', verbose_name='Estado Atual')),
                ('id_Proprietario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='criador', to=settings.AUTH_USER_MODEL, verbose_name='Criador do Ticket')),
                ('prioridade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.prioridade', verbose_name='Prioridade')),
                ('resolucao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.resolucao', verbose_name='Resolução')),
                ('usuario_app', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticket.usuarios_apps')),
                ('usuarios', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='responsavel', to=settings.AUTH_USER_MODEL, verbose_name='Responsável')),
            ],
        ),
        migrations.CreateModel(
            name='Entidades_Apps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.apps', verbose_name='Aplicação')),
                ('entidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.entidades', verbose_name='Utilizador')),
            ],
        ),
        migrations.AddField(
            model_name='apps_tppedidos',
            name='tipoPedidos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticket.tipospedidos', verbose_name='Tipo de Pedido'),
        ),
        migrations.AddField(
            model_name='usuarios',
            name='entidade',
            field=models.ManyToManyField(to='ticket.entidades', verbose_name='Entidades'),
        ),
    ]
