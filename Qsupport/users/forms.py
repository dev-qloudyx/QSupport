from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ticket.models import Usuarios,Entidades,Ticket
from phonenumber_field.modelfields import PhoneNumberField



class InputData(forms.DateInput):
    input_type = 'date'

#Formulário para novos users
class UserRegisterForm(UserCreationForm):
    foto = forms.ImageField()
    date_of_birth = forms.DateField(widget=InputData)
    class Meta:
        model = Usuarios
        fields = ['nome','email','password1','password2','date_of_birth','descricao','role','entidade','foto','telefone']
        exclude = ['']

#Formúlário para os tickets
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nome', 'descricao','app_tpPedidos']

class TicketFormAdmin(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['nome','usuarios','descricao','app_tpPedidos','estado','prioridade']
