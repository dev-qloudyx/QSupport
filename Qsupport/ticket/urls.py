from django.urls import path
from . import views
#from ticket.views import TicketDetalhe

urlpatterns = [
    path("", views.index, name="ticket-home"), #Home Page
    path('novo/', views.create_ticket, name='ticket-novo'), #Criar novo Ticket
    path('criar_entidades/', views.create_entidade, name='criar_entidades'), #URL para criar novos entidades
    path('criar_app/', views.create_apps, name='criar_app'), #URL para criar novos apps
    path('criar_appuser/', views.create_appuser, name='criar_appuser'), #URL para associar utilizadores as suas apps
    path('associar_entid_app/', views.create_entidadeApp, name='associar_entid_app'), #URL para associar entidades as apps
    path('<uuid:uuid>/editar/', views.editar_ticket, name='editar_ticket'),  # Editar ticket
    path('usuarios/alterar_estado/<uuid:uuid>/', views.alterar_estado_usuario, name='alterar_estado_usuario'), #Definir se user está activo ou inativo
    path('tickets/<uuid:uuid>/avancar_estado/', views.avancar_estado_ticket, name='avancar_estado_ticket'), #Avançar o estado de um ticket
    path('tickets/<uuid:uuid>/recuar_estado/', views.recuar_estado_ticket, name='recuar_estado_ticket'), #Recuar o estado de um ticket
    path('tickets/<uuid:uuid>/fechar_estado/', views.fechado_estado_ticket, name='fechado_estado_ticket'), #Recuar o estado de um ticket
    path('<uuid:uuid>/apagar/', views.apagar_ticket, name='apagar_ticket'),  # Apagar ticket
    path('<uuid:uuid>/detalhe', views.ticket_detalhe, name='detalheticket'),  # Ver detalhes do ticket
    path('email/', views.email, name='email'), #URL para enviar mail
    path('tickets/nao_atribuidos/', views.listar_tickets_nao_atribuidos, name='ticketsnaoatribuidos'), #Lista para os operadores escolherem os tickets
    path('tickets/assumir/<uuid:uuid>/', views.assumir_ticket, name='assumir_ticket'), #View para renderizar a função de aceitação do ticket
    path('kanban/', views.lista_kanban, name='listakanban'),
]