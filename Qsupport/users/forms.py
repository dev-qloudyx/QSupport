from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ticket.models import Usuarios,Entidades,Ticket,Apps,Usuarios_Apps, Entidades_Apps
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q,F
from django.core.exceptions import ValidationError



class InputData(forms.DateInput):
    input_type = 'date'

#Formulário para novos users
class UserRegisterFormAdmin(forms.ModelForm):
    foto = forms.ImageField()
    entidade = forms.ModelMultipleChoiceField(
        queryset=Entidades.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    date_of_birth = forms.DateField(widget=InputData,label="Data de Nascimento")
    class Meta:
        model = Usuarios
        fields = ['nome','email','date_of_birth','descricao','role','entidade','foto','telefone']
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

class UserRegisterForm(forms.ModelForm):

    foto = forms.ImageField()
    date_of_birth = forms.DateField(widget=InputData,label="Data de Nascimento")
    class Meta:
        model = Usuarios
        fields = ['nome','email','date_of_birth','foto','telefone']
        exclude = ['password1','password2']
        labels = {
        "nome": "Nome de Utilizador",
        "email":"E-mail",
        "date_of_birth": "Data de Nascimento",
        "foto":"Foto",
        "telefone":"Telefone",
    }
        
class PasswordForm(forms.ModelForm):

    #A form for creating new users. Includes all the required
    #fields, plus a repeated password.

        password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
        password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

        class Meta:
            model = Usuarios
            fields = ('password1','password2')
            
        def clean_password2(self):
            #Verifica se as 2 passwords coincidem
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords não coincidem")
            return password2
        
        def save(self, commit=True):
            # Codifica a password
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user  

        

#Formulário para os tickets
class TicketForm(forms.ModelForm):
    
    def __init__(self,current_user,*args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['usuario_app'].queryset = self.fields['usuario_app'].queryset.exclude(~Q(usuario=current_user))
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
        
#Formulário para associar apps aos users
class AppUserForm(forms.ModelForm):
    
#Criação do filtro de Utilizadores baseados nas Entidades e suas aplicações
   # def __init__(self,current_user,*args, **kwargs):
        #super(AppUserForm, self).__init__(*args, **kwargs)

        #entidades = Entidades_Apps.objects.filter(entidade__nome__in=[current_user.entidade.first()])
        #utilizador = Usuarios.objects.filter(nome = F('nome'))
        #entidades = Entidades_Apps.objects.filter(entidade__nome= utilizador.entidade)

        #self.fields['app'].queryset = entidades

    class Meta:
        model = Usuarios_Apps
        fields = ['usuario','app']
        labels = {
        "usuario": "Utilizador",
        "app":"Aplicação",
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
        "nome": "Nome da Entidade",
        "externo": "A entidade é externa:"
    } 

#Form para associar as entidades as apps
class EntidadeAppForm(forms.ModelForm):

    def __init__(self,current_user,*args, **kwargs):
        super(Entidades_Apps, self).__init__(*args, **kwargs)
    class Meta:
        model = Entidades_Apps
        fields = ['entidade','app']
        labels = {
        "entidade": "Entidade",
        "app":"Aplicação",
    }