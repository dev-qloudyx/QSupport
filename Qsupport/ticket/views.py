from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuarios, Ticket
from users.forms import TicketForm

def index(request):
    listauser = Usuarios.objects.count()
    #Inserir role aqui em vez de nome: nome apenas esta a titulo de exemplo
    filtro = Usuarios.objects.filter(nome="Admin")
    listaadmin = filtro.count()
    return render(request, 'ticket/home.html', context=
        {
            "listaadmin":listaadmin,
            "listauser":listauser,
        })


def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket/gestaodeticket.html', {'tickets': tickets})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.usuarios = request.user
            return redirect('gestao-ticket')
    else:
        form = TicketForm()
    return render(request, 'ticket/novoticket.html', {'form': form})