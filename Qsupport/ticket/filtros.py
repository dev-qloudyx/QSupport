import django_filters
from .models import User, Ticket, Entidades, Apps

#Filtro para a lista de usuários
class UserFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains') 
    id = django_filters.NumberFilter()
    
    class Meta:
        model = User
        fields = ['nome', 'id']

#Filtro para a lista de Ticket
class TicketFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter()
    estado = django_filters.ChoiceFilter(choices=[('2', 'Aberto'), ('6', 'Fechado')])

    class Meta:
        model = Ticket
        fields = ['id', 'estado']

#Filtro para a lista de entidades
class EntidadesFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains') 
    id = django_filters.NumberFilter()
    
    class Meta:
        model = Entidades
        fields = ['nome', 'id']

#Filtro para a lista de Apps
class AppsFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains') 
    id = django_filters.NumberFilter()
    
    class Meta:
        model = Apps
        fields = ['nome', 'id']