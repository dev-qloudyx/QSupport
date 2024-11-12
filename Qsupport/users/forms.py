from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from ticket.models import Usuarios,Entidades,Ticket,Apps,Usuarios_Apps, Entidades_Apps, Comentario
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Q,F
from django.core.exceptions import ValidationError



class InputData(forms.DateInput):
    input_type = 'date'

#Formulário para novos users
class UserRegisterFormAdmin(forms.ModelForm):
    foto = forms.ImageField()
    entidade = forms.ModelMultipleChoiceField(
        queryset=Entidades.objects.exclude(id=3),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    date_of_birth = forms.DateField(widget=InputData,label="Data de Nascimento")
    descricao = forms.CharField(widget=forms.Textarea())
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
        #self.fields['usuario_app'].queryset = self.fields['usuario_app'].queryset.exclude(~Q(usuario=current_user))

        entidades_do_usuario = current_user.entidade.all()
        apps = Apps.objects.filter(entidade__in=entidades_do_usuario)

        self.fields['app'].choices = [(app.id, app.nome) for app in apps]

    descricao = forms.CharField(widget=forms.Textarea(),label="Descrição")
        
    class Meta:
        model = Ticket
        fields = ['app_tpPedidos','nome','descricao','app']
        labels = {
        "app_tpPedidos": "Tipo de problema",
        "nome": "Titulo",
        "descricao":"Descrição",
        "app": "Apps"
    }

#Formulário para os tickets registados internamente
class TicketFormAdmin(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketFormAdmin, self).__init__(*args, **kwargs)
        self.fields['resolucao'].required = False
        self.fields['prioridade'].required = False

    descricao = forms.CharField(widget=forms.Textarea(),label="Descrição")
    class Meta:
        model = Ticket
        fields = ['nome','usuarios','descricao','app_tpPedidos','estado','prioridade', 'app','resolucao']
        labels = {
        "nome": "Titulo",
        "descricao":"Descrição",
        "app_tpPedidos": "Tipo de problema",
        "estado": "Estado",
        "prioridade":"Prioridade",
        "app" : "Aplicação",
        "resolucao":"Resolução"
    }
        
#Formulário para associar apps aos users
class AppUserForm(forms.ModelForm):
    
#Criação do filtro de Utilizadores baseados nas Entidades e suas aplicações
    def __init__(self,*args,current_user,**kwargs):
        super(AppUserForm, self).__init__(*args, **kwargs)

        #entidades = Entidades.objects.filter(~Q(nome__in = teste))
        #utilizador = Usuarios_Apps.objects.filter(~Q(app__entidade__in = teste))
        #entidades = Entidades_Apps.objects.filter(entidade__nome= utilizador.entidade)

        #self.fields['app'].queryset = self.fields['app'].queryset.filter(~Q(entidade__nome__in = teste))
        #print(teste)
        #print(entidades)
        #print(utilizador)

        user_atual = current_user.entidade.all().values("nome")

        filter_query = Q()
        # Vai buscar a lista de entidades do utilizador atual
        filter_list = user_atual # ex:['Qloudyx','Atlas']
        # E adiciona isso a query
        filter_query.add(Q(entidade__nome__in=filter_list), Q.AND)
        print (filter_query)
        print (user_atual)
        self.fields['app'].queryset = self.fields['app'].queryset.filter(filter_query)
        


    class Meta:
        model = Usuarios_Apps
        fields = ['app']
        labels = {
        "app":"Aplicação",
    }
        
#Formulário para registar apps para entidades
class AppsForm(forms.ModelForm):
    class Meta:
        model = Apps
        fields = ['nome','entidade']
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

    #def __init__(self,current_user,*args, **kwargs):
    #    super(Entidades_Apps,self).__init__(*args, **kwargs)
    class Meta:
        model = Entidades_Apps
        fields = ['entidade','app']
        labels = {
        "entidade": "Entidade",
        "app":"Aplicação",
    }
        
#Formulário para os comentários feitos pelos operadores
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 4}),
        }

#Formulário para o comentário final para a resolução
class ComentarioResForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        super(ComentarioResForm, self).__init__(*args, **kwargs)
        #self.fields['resolucao'].queryset = self.fields['resolucao'].queryset.filter(tipo=estado)
        #print(estado)
    class Meta:
        model = Ticket
        fields = ['comresolucao','resolucao']
        widgets = {
            'comresolucao': forms.Textarea(attrs={'rows': 4}),
        }
        