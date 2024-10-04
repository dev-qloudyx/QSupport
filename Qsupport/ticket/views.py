from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuarios, Ticket,Estado, Usuarios_Apps,Entidades, Apps
from users.forms import TicketForm,TicketFormAdmin, AppsForm, EntidadeForm, AppUserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

def index(request):
    corEstado = Estado.objects.filter(cor='Vermelha')
    corEstado = corEstado.last()
    total = Ticket.objects.count()
    filtro = Ticket.objects.filter(estado="1")
    filtroex = Ticket.objects.exclude(estado="1")
    aberto = filtro.count()
    por_abrir = filtroex.count()
    return render(request, 'ticket/home.html', context=
        {
            "total":total,
            "aberto":aberto,
            "por_abrir":por_abrir,
        })

#Ver lista de tickets
def ticket_list(request):
    ticketall = Ticket.objects.all()
    tickuser = request.user
    tickets = Ticket.objects.filter(Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))
    return render(request, 'ticket/listaticket.html', {'tickets': tickets,'ticketall': ticketall})

#ver lista de entidades
def lista_entidades(request):
    entidades = Entidades.objects.all()
    entidade = Entidades.objects.all()
    return render (request,'ticket/listaentidades.html', {'entidade': entidade, 'entidades': entidades})

#ver lista de apps
def lista_apps(request):
    aplicacoes = Apps.objects.all()
    aplicacao = Apps.objects.all()
    return render (request,'ticket/listaaplicacoes.html', {'aplicacao': aplicacao, 'aplicacoes': aplicacoes})

#ver lista de usuários
def lista_user(request):
    usuarios = Usuarios.objects.all()
    usuario =  Usuarios.objects.all()
    return render (request,'ticket/listausuarios.html', {'usuario': usuario, 'usuarios': usuarios})

#Registar um ticket
def create_ticket(request):

    if request.method == 'POST':
        
        form = TicketForm(data=request.POST,current_user=request.user)

        if form.is_valid():
            
            ticket = form.save(commit=False)
            ticket.id_Proprietario = request.user
            ticket = ticket.save()
            #form.save()
            form.instance.usuarios = request.user
            messages.success(request, f'Ticket enviado com sucesso, espere por feedback do nosso operador em serviço.')
            return redirect('listaticket')
    else:
        form = TicketForm(current_user=request.user)
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
                messages.success(request, f'Ticket editado com sucesso.')
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
                messages.success(request, f'Ticket editado com sucesso.')
                return redirect(reverse('listaticket'))
        else:
            form = TicketForm(instance=ticket)
        return render(request, 'ticket/editar_ticket.html', {'form': form, 'ticket': ticket})
    

#Apagar Ticket
@login_required
def apagar_ticket(request, pk):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket, pk=pk)
        #if request.method == 'POST':
        ticket.delete()
        messages.success(request, f'Ticket apagado com sucesso.')
        return redirect('listaticket')
        return render(request, 'ticket/apagar_ticket.html', {'ticket': ticket})
    else:
        ticket = get_object_or_404(Ticket, pk=pk ,usuarios=request.user)
        #if request.method == 'POST':
        ticket.delete()
        messages.success(request, f'Ticket apagado com sucesso.')
        return redirect('listaticket')
        return render(request, 'ticket/apagar_ticket.html', {'ticket': ticket})
    
#Registar nova entidade
def create_entidade(request):
    if request.method == 'POST':
        form = EntidadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Nova entidade criada.')
            return redirect('ticket-home')
    else:
        form = EntidadeForm()
    return render(request, 'ticket/criar_entidades.html', {'form': form})


#Registar nova app
def create_apps(request):
    if request.method == 'POST':
        form = AppsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Nova aplicação criada.')
            return redirect('ticket-home')
    else:
        form = AppsForm()
    return render(request, 'ticket/criar_app.html', {'form': form})

#Registar nova app
def create_appuser(request):
    if request.method == 'POST':
        form = AppUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Nova aplicação criada.')
            return redirect('ticket-home')
    else:
        form = AppUserForm()
    return render(request, 'ticket/criar_appuser.html', {'form': form})