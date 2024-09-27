from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ticket.models import Usuarios,Entidades,Ticket,Apps
from phonenumber_field.modelfields import PhoneNumberField



class InputData(forms.DateInput):
    input_type = 'date'

#Formulário para novos users
class UserRegisterForm(UserCreationForm):
    foto = forms.ImageField()
    date_of_birth = forms.DateField(widget=InputData,label="Data de Nascimento")
    class Meta:
        model = Usuarios
        fields = ['nome','email','password1','password2','date_of_birth','descricao','role','entidade','foto','telefone']
        exclude = ['']
        labels = {
        "nome": "Nome de Utilizador",
        "email":"E-mail",
        "date_of_birth": "Data de Nascimento",
        "descricao": "Descrição",
        "role":"Cargo",
        "entidade":"Entidade",
        "foto":"Foto",
        "telefone":"Telefone",
    }

        

#Formulário para os tickets
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nome', 'descricao','app_tpPedidos', 'usuario_app']
        labels = {
        "nome": "Titulo",
        "descricao":"Descrição",
        "app_tpPedidos": "Tipo de problema",
        "usuario_app" : "Aplicação"
    }

#Formulário para os tickets registados internamente
class TicketFormAdmin(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nome','usuarios','descricao','app_tpPedidos','estado','prioridade', 'usuario_app']
        labels = {
        "nome": "Titulo",
        "descricao":"Descrição",
        "app_tpPedidos": "Tipo de problema",
        "estado": "Estado",
        "prioridade":"Prioridade",
        "usuario_app" : "Aplicação",
    }
        
#Formulário para registar apps para entidades
class AppsForm(forms.ModelForm):
    class Meta:
        model = Apps
        fields = ['nome']
        labels = {
        "nome": "Nome da App"
    }
        
#Formulário para registar as entidades
class EntidadeForm(forms.ModelForm):
    class Meta:
        model = Entidades
        fields = ['nome', 'externo']
        labels = {
        "nome": "Nome da App",
        "externo": "A entidade é externa:"
    } 


