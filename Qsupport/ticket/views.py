from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuarios, Ticket,Estado, Usuarios_Apps,Entidades, Apps, Comentario
from users.forms import TicketForm,TicketFormAdmin, AppsForm, EntidadeForm, AppUserForm, EntidadeAppForm, ComentarioForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .filtros import UserFilter, TicketFilter, EntidadesFilter, AppsFilter


def index(request):
    corEstado = Estado.objects.filter(cor='Vermelha')
    corEstado = corEstado.last()
    total = Ticket.objects.count()
    filtro = Ticket.objects.filter(estado="1")
    filtroex = Ticket.objects.exclude(estado="1")
    designados = Ticket.objects.exclude(usuarios__isnull=True)
    aberto = filtro.count()
    por_abrir = filtroex.count()
    designado = designados.count()
    return render(request, 'ticket/home.html', context=
        {
            "total":total,
            "aberto":aberto,
            "por_abrir":por_abrir,
            "designado": designado,
        })

#Ver lista de tickets
def ticket_list(request):
    ticketall = Ticket.objects.all()
    tickuser = request.user
    tickets = Ticket.objects.filter(Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))
    ticketfilter = TicketFilter(request.GET, ticketall)
    total_resultados = ticketfilter.qs.count()
    return render(request, 'ticket/listaticket.html', {'tickets': tickets,'ticketall': ticketfilter.qs, 'filter':ticketfilter, 'total':total_resultados})

#ver lista de entidades
def lista_entidades(request):
    entidade = Entidades.objects.all()
    entfiltro = EntidadesFilter(request.GET, entidade)
    total_resultados = entfiltro.qs.count()
    return render (request,'ticket/listaentidades.html', {'entidade': entfiltro.qs, 'total':total_resultados, 'filter':entfiltro})

#ver lista de apps
def lista_apps(request):
    aplicacao = Apps.objects.all()
    appfiltro = AppsFilter(request.GET, aplicacao)
    total_resultados = appfiltro.qs.count()
    return render (request,'ticket/listaaplicacoes.html', {'total':total_resultados, 'aplicacao': appfiltro.qs, 'filter':appfiltro})

#ver lista de usuários
def lista_user(request):
    usuario =  Usuarios.objects.all()
    userfiltro = UserFilter(request.GET, usuario)
    total_resultados = userfiltro.qs.count()
    return render (request,'ticket/listausuarios.html', {'total':total_resultados,'usuario': userfiltro.qs, 'filter':userfiltro})

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
def ticket_detalhe(request, uuid):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket, uuid=uuid)
        comentarios = ticket.comentarios.all()
        #view para adicionar novo comentário
        if request.method == 'POST':
            form = ComentarioForm(request.POST)
            
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.ticket = ticket
                comentario.operador = request.user
                comentario.save()
                return redirect('detalheticket', uuid=ticket.uuid)
        else:
            form = ComentarioForm()
        
        return render(request, 'ticket/detalheticket.html', {
            'ticket': ticket,
            'comentarios': comentarios,
            'form': form,
        })
    else:
        ticket = get_object_or_404(Ticket, uuid=uuid)
        return render(request, 'ticket/detalheticket.html', {'ticket': ticket})

#Editar Ticket
@login_required
def editar_ticket(request, uuid):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket,uuid=uuid)
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
        ticket = get_object_or_404(Ticket,uuid=uuid,usuarios=request.user)
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
def apagar_ticket(request, uuid):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        ticket = get_object_or_404(Ticket, uuid=uuid)
        #if request.method == 'POST':
        ticket.delete()
        messages.success(request, f'Ticket apagado com sucesso.')
        return redirect('listaticket')
        return render(request, 'ticket/apagar_ticket.html', {'ticket': ticket})
    else:
        ticket = get_object_or_404(Ticket, uuid=uuid ,usuarios=request.user)
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

#Associar users as apps
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


def email(request):
    
    login = request.user
    emailto = request.user.email

    html_content = render_to_string(
    "users/requisitarpass.html",
    context={"id": login},
    )

    email = EmailMultiAlternatives('Definição de palavra-passe',"teste",settings.EMAIL_HOST_USER,[emailto])
    email.attach_alternative(html_content, "text/html")
    email.send()
    messages.success(request, f'E-mail a requisitar a palavra-passe enviado.')
    return redirect('ticket-home')



#Associar entidades as apps
def create_entidadeApp(request):
    if request.method == 'POST':
        form = EntidadeAppForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Entidade e app associadas com sucesso.')
            return redirect('ticket-home')
    else:
        form = EntidadeAppForm(current_user=request.user)
    return render(request, 'ticket/associar_entid_app.html', {'form': form})