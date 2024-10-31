import django_filters
from .models import User, Ticket, Entidades, Apps

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
    id = django_filters.NumberFilter()
    estado = django_filters.ChoiceFilter(choices=[('1', 'Aberto'), ('6', 'Fechado')])
    prioridade = django_filters.ChoiceFilter(choices=[('1', 'Baixa'), 
        ('2', 'Media'), 
        ('3', 'Alta'), 
        ('4', 'Critica'), 
        ('5', 'Cancelado')])
    id_Proprietario_nome = django_filters.CharFilter(field_name="id_Proprietario__nome",lookup_expr='icontains')
    app = django_filters.CharFilter(field_name="app__nome",lookup_expr='icontains')
    usuarios = django_filters.CharFilter(field_name="usuarios__nome",lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = ['id', 'estado', 'id_Proprietario', 'app', 'usuarios']

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