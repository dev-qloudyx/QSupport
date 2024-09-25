from django.urls import path
from . import views
#from ticket.views import TicketDetalhe

urlpatterns = [
    path("", views.index, name="ticket-home"), #Home Page
    path('novo/', views.create_ticket, name='ticket-novo'), #Criar novo Ticket
    path('<int:pk>/editar/', views.editar_ticket, name='editar_ticket'),  # Editar ticket
    path('<int:pk>/apagar/', views.apagar_ticket, name='apagar_ticket'),  # Apagar ticket
    path('<int:pk>/detalhe', views.ticket_detalhe, name='detalheticket'),  # Ver detalhes do ticket
]