from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Usuarios, Ticket,Estado
from users.forms import TicketForm

def index(request):
    listauser = Usuarios.objects.count()
    lastuser = Usuarios.objects.last()
    corEstado = Estado.objects.filter(cor='Vermelha')
    corEstado = corEstado.last()
    #Inserir role aqui em vez de nome: nome apenas esta a titulo de exemplo
    filtro = Usuarios.objects.filter(nome="Admin")
    lastadmin = filtro.last()
    listaadmin = filtro.count()
    return render(request, 'ticket/home.html', context=
        {
            "listaadmin":listaadmin,
            "listauser":listauser,
            "lastadmin":lastadmin,
            "lastuser":lastuser,
            "corEstado":corEstado,
        })


def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket/gestaodeticket.html', {'tickets': tickets})

def ticket_listteste(request):
    tickets = Ticket.objects.all()
    return render(request, 'ticket/gestaodeticketteste.html', {'tickets': tickets})


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            form.instance.usuarios = request.user
            messages.success(request, f'Ticket enviado com sucesso, espere por feedback do nosso operador em serviço.')
            return redirect('ticket-gestao')
    else:
        form = TicketForm()
    return render(request, 'ticket/novoticket.html', {'form': form})