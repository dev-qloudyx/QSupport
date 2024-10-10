from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterFormAdmin,UserRegisterForm, TicketForm, PasswordForm
from ticket.models import Usuarios, Ticket
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

#registar novos usuários
def register(request):
    if request.method == 'POST':
        form = UserRegisterFormAdmin(request.POST, request.FILES)
        palavra_passe = "AdminAdmin"
        makepass = make_password(palavra_passe)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = makepass
            user = user.save()
            #form.save()
                
            login = Usuarios.objects.last()
            email = login.objects.email()

            html_content = render_to_string(
            "users/requisitarpass.html",
            context={"id": login},
            )

            email = EmailMultiAlternatives('Definição de palavra-passe',"teste",settings.EMAIL_HOST_USER,[email])
            email.attach_alternative(html_content, "text/html")
            email.send()
            messages.success(request, f'Registo completo, O novo utilizador vai agora receber um e-mail para definir a sua palavra-passe.')
            return redirect('ticket-home')
        
    else:
        form = UserRegisterFormAdmin()
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

#Editar Utilizador
@login_required
def editar_user(request, uuid):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        utilizador = get_object_or_404(Usuarios,uuid=uuid)
        if request.method == 'POST':
            form = UserRegisterFormAdmin(request.POST, instance=utilizador)
            if form.is_valid():
                form.save()
                messages.success(request, f'Utilizador editado com sucesso.')
                return redirect('profile')
        else:
            form = UserRegisterFormAdmin(instance=utilizador)
        return render(request, 'users/profileedit.html', {'form': form, 'utilizador': utilizador})
    else:
        utilizador = get_object_or_404(Usuarios,uuid=uuid)
        if request.method == 'POST':
            form = UserRegisterForm(request.POST, instance=utilizador)
            if form.is_valid():
                form.save()
                messages.success(request, f'Utilizador editado com sucesso.')
                return redirect('profile')
        else:
            form = UserRegisterForm(instance=utilizador)
        return render(request, 'users/profileedit.html', {'form': form, 'utilizador': utilizador})
    
#@login_required
def editar_pass(request, uuid):
    if request.user.is_authenticated:
        if request.user.nome == "Admin" or request.user.role == "Interno":
            utilizador = get_object_or_404(Usuarios,uuid=uuid)
            if request.method == 'POST':
                form = PasswordForm(request.POST, instance=utilizador)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Password editada com sucesso, por favor volte a entrar com a sua conta')
                    return redirect('logout')
            else:
                form = PasswordForm(instance=utilizador)
            return render(request, 'users/passwordedit.html', {'form': form, 'utilizador': utilizador})
        else:
            utilizador = get_object_or_404(Usuarios,uuid=uuid)
            if request.method == 'POST':
                form = PasswordForm(request.POST, instance=utilizador)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Password editada com sucesso, por favor volte a entrar com a sua conta')
                    return redirect('logout')
            else:
                form = PasswordForm(instance=utilizador)
            return render(request, 'users/passwordedit.html', {'form': form, 'utilizador': utilizador})
    else:
        utilizador = get_object_or_404(Usuarios,uuid=uuid)
        user = "Registo"
        password = "AdminAdmin"
        new_user = authenticate(username=user,
                                password=password,
                                )
        login(request, new_user) 
        if request.method == 'POST':
                form = PasswordForm(request.POST, instance=utilizador)
                if form.is_valid():
                    form.save()
                    messages.success(request, f'Password editada com sucesso, por favor volte a entrar com a sua conta')
                    return redirect('logout')
        else:
                form = PasswordForm(instance=utilizador)
        return render(request, 'users/passwordedit.html', {'form': form, 'utilizador': utilizador})
    
        