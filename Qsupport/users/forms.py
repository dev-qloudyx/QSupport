from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ticket.models import Usuarios,Entidades
from phonenumber_field.modelfields import PhoneNumberField



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    nome = forms.CharField(max_length=120)
    #foto = forms.ImageField()
    descricao = forms.CharField(max_length=250)
    role = forms.CharField(max_length=50)
    entidade = forms.CharField(max_length=200)
    telefone = PhoneNumberField()
    
    #ideia: criar outro Register Form abaixo deste com as credenciais da tabela Usuarios
    class Meta:
        model = User
        fields = ['username','nome','email','password1','password2']
        exclude = ['']