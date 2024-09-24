from django.urls import path
from . import views
#from ticket.views import TicketDetalhe

urlpatterns = [
    path("", views.index, name="ticket-home"),
    path('gestao/', views.ticket_list, name='ticket-gestao'),
    path('novo/', views.create_ticket, name='ticket-novo'),
    #TicketDetalhe.as_view()
    path('detalhe/', views.profile_ticket , name='ticket-detalhe'), #Detalhe ticket
    path('gestaoteste/', views.ticket_listteste, name='ticket-gestaot'),
    path('edit/', views.editar_ticket, name='editar-ticket'),  # Editar ticket, usar <int:pk> atras do link
    path('delete/', views.apagar_ticket, name='apagar-ticket'), # Apagar ticket, usar <int:pk> atras do link
]