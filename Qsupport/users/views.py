from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TicketForm
from ticket.models import Usuarios, Ticket
from django.http import Http404


#registar novos usuários
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Conta criada com sucesso, já pode logar!')
            return redirect ('ticket-home')
        
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

#Acesso ao perfil apenas quando logado
@login_required
def profile(request):
    total = Ticket.objects.count()
    
    #Tickets Resolvidos
    filtroresolvido = Ticket.objects.filter(estado="3")
    resolvido = filtroresolvido.count()
    percentresolvido = int(resolvido / total * 100)

    #Tickets Criticos
    filtrocritico = Ticket.objects.filter(prioridade="4")
    critico = filtrocritico.count()
    percentcritico = int(critico / total * 100)

    #Ticket Prioridade Alta
    filtroalto = Ticket.objects.filter(prioridade="3")
    alto = filtroalto.count()
    percentalto = int(alto / total * 100)

    #Tickets Prioridade Media
    filtromedio = Ticket.objects.filter(prioridade="2")
    medio = filtromedio.count()
    percentmedio = int(medio / total * 100)

    #Tickets Prioridade Baixa
    filtrobaixo = Ticket.objects.filter(prioridade="1")
    baixo = filtrobaixo.count()
    percentbaixo = int(baixo / total * 100)


    return render (request, 'users/profile.html',context = 
                   {
                    'resolvido':percentresolvido,
                    'critico':percentcritico,
                    'alto':percentalto,
                    'medio':percentmedio,
                    'baixo':percentbaixo,
                   }
                   )