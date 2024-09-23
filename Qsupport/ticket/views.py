from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuarios, Ticket, StatusLog
from users.forms import TicketForm
from django.contrib.auth.decorators import login_required

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
    tickets = Ticket.objects.all(usuarios=request.user)
    return render(request, 'ticket/gestaodeticket.html', {'tickets': tickets})

def ticket_estatus(request):
    estado = StatusLog.objects.all(usuarios=request.user)
    return render(request, 'ticket/gestaodeticket.html', {'estado': estado})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.usuario = request.user
            ticket.save()
            return redirect('gestao-ticket')
    else:
        form = TicketForm()
    return render(request, 'ticket/novoticket.html', {'form': form})