from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ticket-home"),
    path('gestao/', views.ticket_list, name='ticket-gestao'),
    path('novo/', views.create_ticket, name='ticket-novo'),
    path('gestaoteste/', views.ticket_listteste, name='ticket-gestaot'),
]