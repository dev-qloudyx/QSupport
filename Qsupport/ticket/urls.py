from django.urls import path
from . import views
#from ticket.views import TicketDetalhe

urlpatterns = [
    path("", views.index, name="ticket-home"), #Home Page
    path('novo/', views.create_ticket, name='ticket-novo'), #Criar novo Ticket
    path('criar_entidades/', views.create_entidade, name ='criar_entidades'), #URL para criar novos entidades
    path('criar_app/', views.create_apps, name ='criar_app'), #URL para criar novos apps
    path('<int:pk>/editar/', views.editar_ticket, name='editar_ticket'),  # Editar ticket
    path('<int:pk>/apagar/', views.apagar_ticket, name='apagar_ticket'),  # Apagar ticket
    path('<int:pk>/detalhe', views.ticket_detalhe, name='detalheticket'),  # Ver detalhes do ticket
]