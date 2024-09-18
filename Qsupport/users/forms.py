from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ticket.models import Usuarios,Entidades
from phonenumber_field.modelfields import PhoneNumberField



class UserRegisterForm(UserCreationForm):
    class Meta:
        model = Usuarios
        fields = ['nome','email','password1','password2','date_of_birth','descricao','role','entidade','foto','telefone']
        exclude = ['']