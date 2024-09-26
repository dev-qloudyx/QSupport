from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Usuarios, Ticket,Estado
from users.forms import TicketForm,TicketFormAdmin
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

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
    ticketall = Ticket.objects.all()
    tickuser = request.user
    tickets = Ticket.objects.filter(Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))
    return render(request, 'ticket/listaticket.html', {'tickets': tickets,'ticketall': ticketall})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.id_Proprietario = request.user
            ticket = ticket.save()
            #form.save()
            form.instance.usuarios = request.user
            messages.success(request, f'Ticket enviado com sucesso, espere por feedback do nosso operador em serviço.')
            return redirect('listaticket')
    else:
        form = TicketForm()
    return render(request, 'ticket/novoticket.html', {'form': form})

#Ver detalhes do ticket
@login_required
def ticket_detalhe(request, pk):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket, pk=pk)
        return render(request, 'ticket/detalheticket.html', {'ticket': ticket})
    else:
        ticket = get_object_or_404(Ticket, pk=pk)
        return render(request, 'ticket/detalheticket.html', {'ticket': ticket})

#Editar Ticket
@login_required
def editar_ticket(request, pk):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket,pk=pk)
        if request.method == 'POST':
            form = TicketFormAdmin(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect(reverse('listaticket'))
        else:
            form = TicketFormAdmin(instance=ticket)
        return render(request, 'ticket/editar_ticket.html', {'form': form, 'ticket': ticket})
    else:
        ticket = get_object_or_404(Ticket,pk=pk,usuarios=request.user)
        if request.method == 'POST':
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect(reverse('listaticket'))
        else:
            form = TicketForm(instance=ticket)
        return render(request, 'ticket/editar_ticket.html', {'form': form, 'ticket': ticket})
    

#Apagar Ticket
@login_required
def apagar_ticket(request, pk):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket, pk=pk)
        if request.method == 'POST':
            ticket.delete()
            return redirect('listaticket')
        return render(request, 'ticket/apagar_ticket.html', {'ticket': ticket})
    else:
        ticket = get_object_or_404(Ticket, pk=pk ,usuarios=request.user)
        if request.method == 'POST':
            ticket.delete()
            return redirect('listaticket')
        return render(request, 'ticket/apagar_ticket.html', {'ticket': ticket})