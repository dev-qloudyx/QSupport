from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (Usuarios,
    Ticket,
    Estado,
    Usuarios_Apps,
    Entidades,
    Apps,
    Comentario,
    StatusLog,
    AcaoEstado,
    Resolucao)
from users.forms import (TicketForm,
    TicketFormAdmin,
    AppsForm,
    EntidadeForm,
    AppUserForm,
    EntidadeAppForm,
    ComentarioForm,
    ComentarioResForm,
    ComentarioResForm2)
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.db.models import Q
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .filtros import UserFilter, TicketFilter, EntidadesFilter, AppsFilter, KanbanFilter
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json


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

#Função para apanhar o admin
def is_admin(user):
    return user.is_admin

#Ver lista de tickets
def ticket_list(request):
    ticketall = Ticket.objects.all()
    tickuser = request.user
    tickets = Ticket.objects.filter(Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))
    cliente = Ticket.objects.filter(id_Proprietario=tickuser)
    aberto = request.GET.get('aberto')
    ordem = request.GET.get('ordem')
    if (aberto == "1"):
        ticketall = Ticket.objects.all().exclude(Q(estado=6) | Q(estado=7))
    if (aberto == "2"):
        ticketall = Ticket.objects.all().filter(Q(estado=6) | Q(estado=7))
    if (ordem == "1"):
        ticketall = ticketall.order_by("id")
    if (ordem == "-1"):
        ticketall = ticketall.order_by("-id")
    if (ordem == "2"):
        ticketall = ticketall.order_by("prioridade")
    if (ordem == "-2"):
        ticketall = ticketall.order_by("-prioridade")
    if (ordem == "3"):
        ticketall = ticketall.order_by("app")
    if (ordem == "-3"):
        ticketall = ticketall.order_by("-app")    
    if (ordem == "4"):
        ticketall = ticketall.order_by("nome")
    if (ordem == "-4"):
        ticketall = ticketall.order_by("-nome")
    if (ordem == "5"):
        ticketall = ticketall.order_by("id_Proprietario")
    if (ordem == "-5"):
        ticketall = ticketall.order_by("-id_Proprietario")
    if (ordem == "6"):
        ticketall = ticketall.order_by("dataCriacao")
    if (ordem == "-6"):
        ticketall = ticketall.order_by("-dataCriacao")
    if (ordem == "7"):
        ticketall = ticketall.order_by("usuarios")
    if (ordem == "-7"):
        ticketall = ticketall.order_by("-usuarios")
    if (ordem == "8"):
        ticketall = ticketall.order_by("dataAtualizacao")
    if (ordem == "-8"):
        ticketall = ticketall.order_by("-dataAtualizacao")
    if (ordem == "9"):
        ticketall = ticketall.order_by("estado")
    if (ordem == "-9"):
        ticketall = ticketall.order_by("-estado")
    
    ticketfilter = TicketFilter(request.GET, ticketall)
    ticketfilteroperador = TicketFilter(request.GET, tickets)
    ticketfiltercliente = TicketFilter(request.GET, cliente)
    total_resultados = ticketfilter.qs.count()
    estado_filtro = request.GET.get('estado')
    paginator = Paginator(ticketfilter.qs,2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    #filtros rápidos
    #if estado_filtro == 'abertos':
    #    tickets = Ticket.objects.exclude(Q(estado__estado=6) | Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))
    #elif estado_filtro == 'fechados':
    #    tickets = Ticket.objects.filter(Q(estado__estado=6) | Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))
    #else:
    #    tickets = Ticket.objects.filter(Q(usuarios=tickuser) | Q(id_Proprietario=tickuser))

    return render(request, 'ticket/listaticket.html', 
                  {'tickets': ticketfilteroperador.qs,
                   'ticketall': ticketfilter.qs, 
                   'cliente':ticketfiltercliente.qs,
                   'filter':ticketfilter, 
                   'total':total_resultados,
                   'page_obj':page_obj,
                   'paginator':paginator,})

#Lista em modelo Kanban
def lista_kanban(request):
    estados = Estado.objects.order_by("id")
    tickets_por_estado = {estado: Ticket.objects.filter(estado=estado) for estado in estados}

    #filtros para o kanban
    ticket = Ticket.objects.all()
    ticketfilter= KanbanFilter(request.GET, ticket)
    
    return render(request, 'ticket/listakanban.html', {
        'tickets_por_estado': tickets_por_estado,
        'estados': estados,
        'filter':ticketfilter,
    })

#Mudar estado no Kanban
@require_POST
def mudar_estado_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        novo_estado_nome = request.POST.get("estado")
        novo_estado = Estado.objects.get(estado=novo_estado_nome)
        ticket.estado = novo_estado
        ticket.save()

        return JsonResponse({'success': True})
    except Ticket.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Ticket não encontrado'})
    except Estado.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Estado não encontrado'})

#Dashboard
def tickets_charts(request):
    data = Ticket.objects.all().order_by('dataCriacao')  # Ordene por data
    result = {
        "labels": [item.dataCriacao.strftime("%Y-%m-%d") for item in data],
        "values": [item.uuid for item in data],
    }
    final = JsonResponse(result)
    html = render_to_string("ticketcharts.html",final)
    serialized_data = json.dumps({"html":html})
    return HttpResponse(serialized_data,content_type='application/json')
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
            ticket.app = Apps.objects.get(nome=form.cleaned_data['app'])
            ticket = ticket.save()
            #form.save()
            form.instance.usuarios = request.user
            seguinte = Ticket.objects.filter().last()
            seguinte = get_object_or_404(Ticket, nome=seguinte)
            defeito = Estado.objects.filter(estado="Aberto").last()
            defeito = get_object_or_404(Estado, estado=defeito)
            print(defeito)
            historico = StatusLog(ticket = seguinte , estado = defeito , usuario = request.user)
            historico.save()
            
            messages.success(request, f'Ticket enviado com sucesso, espere por feedback do nosso operador em serviço.')
            return redirect('listaticket')
    else:
        form = TicketForm(current_user=request.user)
    return render(request, 'ticket/novoticket.html', {'form': form})

#Ver detalhes do ticket
@login_required
def ticket_detalhe(request, uuid):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        seguinte = None
        anterior = None
        ticket = get_object_or_404(Ticket, uuid=uuid)
        tickets = get_object_or_404(Ticket, uuid=uuid)

        if ticket.estado.id > 1:
            anterior = StatusLog.objects.filter(ticket = ticket.id).last() # Estado Anterior
            anterior = get_object_or_404(Estado, estado = anterior) # Vai buscar os dados do Estado do StatusLogs
            anterior = StatusLog.objects.filter(ticket = ticket.id).exclude(estado = anterior.id).last() # Estado antes do ultimo
            anterior = get_object_or_404(Estado, estado = anterior) # Vai buscar os dados do Estado do StatusLogs Excluindo o ultimo anterior
        if ticket.estado.id < 6:
            seguinte = AcaoEstado.objects.filter(inicio = ticket.estado) # Estado Seguinte
            print(seguinte)
        comentarios = ticket.comentarios.all()
        #view para adicionar novo comentário (form) ou comentário de resolução (formfechado ou formcancelado)
        
        if request.method == 'POST':
            form = ComentarioForm(request.POST)
            formfechado = ComentarioResForm(request.POST, instance=ticket)
            formcancelado = ComentarioResForm2(request.POST,instance=ticket)
           
            
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.ticket = ticket
                comentario.operador = request.user
                comentario.save()
                return redirect('detalheticket', uuid=ticket.uuid)
            
            if formfechado.is_valid():
                comentario = request.POST['comresolucao']
                resolve = request.POST['resolucao']
                num = request.POST.get('valor')
                Ticket.objects.filter(uuid=ticket.uuid).update(comresolucao = comentario, resolucao = resolve)
                Ticket.objects.filter(id = tickets.id).update(estado = num)
                Ticket.objects.filter(id = tickets.id).update(dataAtualizacao = timezone.now())
                tickets = get_object_or_404(Ticket, uuid=uuid) #Vai buscar os novos dados para guardar no StatusLogs
                historico = StatusLog(ticket = tickets , estado = tickets.estado , usuario = request.user) #Prepara os dados para guardar
                historico.save()
                messages.success(request, f'Comentário de resolução adicionado.')
                return redirect('detalheticket', uuid=ticket.uuid)
            
            if formcancelado.is_valid():
                comentario = request.POST['comresolucao']
                resolve = request.POST['resolucao']
                num = request.POST.get('valor')
                Ticket.objects.filter(uuid=ticket.uuid).update(comresolucao = comentario, resolucao = resolve)
                Ticket.objects.filter(id = tickets.id).update(estado = num)
                Ticket.objects.filter(id = tickets.id).update(dataAtualizacao = timezone.now())
                tickets = get_object_or_404(Ticket, uuid=uuid) #Vai buscar os novos dados para guardar no StatusLogs
                historico = StatusLog(ticket = tickets , estado = tickets.estado , usuario = request.user) #Prepara os dados para guardar
                historico.save()
                messages.success(request, f'Comentário de resolução adicionado.')
                return redirect('detalheticket', uuid=ticket.uuid)
            
        else:
            
            form = ComentarioForm()
            formfechado = ComentarioResForm(instance=ticket)
            formcancelado = ComentarioResForm2(instance=ticket)
            
        
        return render(request, 'ticket/detalheticket.html', {
            'ticket': ticket,
            'seguinte': seguinte,
            'anterior': anterior,
            'comentarios': comentarios,
            'form': form,
            'form2':formfechado,
            'form3':formcancelado,
        })
    else:
        ticket = get_object_or_404(Ticket, uuid=uuid)
        return render(request, 'ticket/detalheticket.html', {'ticket': ticket})
    
        
#Avançar os estados via botão
@login_required
def avancar_estado_ticket(request, uuid):
    
    tickets = get_object_or_404(Ticket, uuid=uuid)
    if request.user.nome == "Admin" or request.user.role == "Interno":
            num = request.POST.get('valor')
            Ticket.objects.filter(id = tickets.id).update(estado = num)
            Ticket.objects.filter(id = tickets.id).update(dataAtualizacao = timezone.now())
            tickets = get_object_or_404(Ticket, uuid=uuid) #Vai buscar os novos dados para guardar no StatusLogs
            historico = StatusLog(ticket = tickets , estado = tickets.estado , usuario = request.user) #Prepara os dados para guardar
            historico.save()
            messages.success(request, 'O estado do ticket foi atualizado para o próximo estado.')
    else:
        messages.error(request, 'Você não tem permissão para alterar o estado deste ticket.')
    
    return redirect('detalheticket', uuid=tickets.uuid)

#Recuar estado via botão
@login_required
def recuar_estado_ticket(request, uuid):
    ticket = get_object_or_404(Ticket, uuid=uuid)

    if request.user.nome == "Admin" or request.user.role == "Interno":
            apagar = StatusLog.objects.filter(ticket = ticket.id).last()
            apagar.delete()
            antes = StatusLog.objects.filter(ticket = ticket.id).last()
            antes = get_object_or_404(Estado, estado = antes)
            Ticket.objects.filter(id = ticket.id).update(estado = antes)
            Ticket.objects.filter(id = ticket.id).update(dataAtualizacao = timezone.now())
            messages.success(request, 'O estado do ticket foi alterado para o estado anterior.')
    else:
        messages.error(request, 'Você não tem permissão para alterar o estado deste ticket.')
    
    return redirect('detalheticket', uuid=ticket.uuid)

#Fechar o ticket
@login_required
def fechado_estado_ticket(request, uuid):
    ticket = get_object_or_404(Ticket, uuid=uuid)

    if request.user.nome == "Admin" or request.user.role == "Interno":
            Ticket.objects.filter(id = ticket.id).update(estado = 6)
            Ticket.objects.filter(id = ticket.id).update(dataAtualizacao = timezone.now())
            tickets = get_object_or_404(Ticket, uuid=uuid)
            historico = StatusLog(ticket = tickets , estado = tickets.estado , usuario = request.user)
            historico.save()
            messages.success(request, 'O ticket foi encerrado.')
    else:
        messages.error(request, 'Você não tem permissão para alterar o estado deste ticket.')
    
    return redirect('detalheticket', uuid=ticket.uuid)


#Editar Ticket
@login_required
def editar_ticket(request, uuid):
    if request.user.nome == "Admin" or request.user.role == "Interno":
        tickets = get_object_or_404(Ticket,uuid=uuid)
        if request.method == 'POST':
            form = TicketFormAdmin(request.POST, instance=tickets)
            if form.is_valid():
                gravar = form.save(commit=False)
                gravar.dataAtualizacao = timezone.now()
                gravar = gravar.save()
                #form.save()
                historico = StatusLog(ticket = tickets , estado = tickets.estado , usuario = request.user)
                historico.save()
                messages.success(request, f'Ticket editado com sucesso.')
                return redirect(reverse('listaticket'))
        else:
            form = TicketFormAdmin(instance=tickets)
        return render(request, 'ticket/editar_ticket.html', {'form': form, 'ticket': tickets})
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
        
        form = AppUserForm(request.POST,current_user=request.user)
        if form.is_valid():
            link = form.save(commit=False)
            link.usuario = request.user
            link = link.save()
            messages.success(request, f'Nova aplicação criada.')
            return redirect('ticket-home')
    else:
        form = AppUserForm(current_user=request.user)
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
        form = EntidadeAppForm()#current_user=request.user)
    return render(request, 'ticket/associar_entid_app.html', {'form': form})

#Lista de tickets não atribuídos
@login_required
def listar_tickets_nao_atribuidos(request):
    tickets_nao_atribuidos = Ticket.objects.filter(usuarios__isnull=True, estado=1)
    return render(request, 'ticket/ticketsnaoatribuidos.html', {'tickets': tickets_nao_atribuidos})

#View para atribuir um operador ao ticket
@login_required
def assumir_ticket(request, uuid):
    tickets = Ticket.objects.get(uuid=uuid)
    
    if tickets.usuarios is None:
        tickets.usuarios = request.user
        tickets.save()

    tickets = Ticket.objects.get(uuid=uuid)
    #historico = StatusLog(ticket = tickets , estado = tickets.estado , usuario = request.user)
    #historico.save()
    return redirect('ticketsnaoatribuidos')

#Activar e desativar users
@user_passes_test(is_admin)
def alterar_estado_usuario(request, uuid):
    usuario = get_object_or_404(Usuarios, uuid=uuid)
    
    if usuario.is_active:
        usuario.is_active = False
    else:
        usuario.is_active = True

    usuario.save()

    return redirect('listausuarios')

