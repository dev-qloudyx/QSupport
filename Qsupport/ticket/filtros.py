import django_filters
from .models import User, Ticket, Entidades, Apps, Estado
from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404

#Filtro para a lista de usuários
class UserFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains') 
    id = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter(field_name="is_active")
    
    class Meta:
        model = User
        fields = ['nome', 'id', 'is_active']

#Filtro para a lista de Ticket
class TicketFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(label="ID - Ticket")
    estado = django_filters.MultipleChoiceFilter(choices=[('1', 'Aberto'),('6', 'Descartado'),('7','Fechado')],widget = (forms.CheckboxSelectMultiple()))
    prioridade = django_filters.ChoiceFilter(choices=[('1', 'Baixa'), 
        ('2', 'Media'), 
        ('3', 'Alta'), 
        ('4', 'Critica'), 
        ('5', 'Cancelado')])
    id_Proprietario = django_filters.CharFilter(field_name="id_Proprietario__nome",lookup_expr='icontains',label="Criado por")
    app = django_filters.CharFilter(field_name="app__nome",lookup_expr='icontains',label="Aplicação")
    usuarios = django_filters.CharFilter(field_name="usuarios__nome",lookup_expr='icontains',label="Responsável")

    class Meta:
        model = Ticket
        fields = ['id', 'id_Proprietario', 'app', 'usuarios','prioridade', 'estado']
        

#Filtro para a lista de entidades
class EntidadesFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains') 
    id = django_filters.NumberFilter()
    externo = django_filters.BooleanFilter(field_name="externo")
    
    class Meta:
        model = Entidades
        fields = ['nome', 'id', 'externo']

#Filtro para a lista de Apps
class AppsFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains') 
    id = django_filters.NumberFilter()
    ativo = django_filters.BooleanFilter(field_name="ativo")
    
    class Meta:
        model = Apps
        fields = ['nome', 'id', 'ativo']