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
            return redirect ('login')
        
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

#Acesso ao perfil apenas quando logado
@login_required
def profile(request):
    return render (request, 'users/profile.html')