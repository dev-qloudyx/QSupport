from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuarios

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


