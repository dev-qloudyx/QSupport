from django import forms
from .models import Usuarios


foto = forms.ImageField(
    label="Foto de Perfil", 
    widget= forms.ClearableFileInput(attrs={
        'class': 'form-control'
        })
        ),