from django import forms
from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Usuarios,Estado,Entidades,Resolucao,Prioridade,TiposPedidos,Apps,Usuarios_Apps,Apps_tpPedidos,Ticket,StatusLog 

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Usuarios
        fields = ('nome','email','date_of_birth','descricao','role','foto','telefone')

    def clean_password2(self):
        # Verifica se as 2 passwords coincidem
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        # Codifica a password
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Usuarios
        fields = ('nome','email', 'password','descricao','date_of_birth','is_active','is_admin')


class UserAdmin(BaseUserAdmin):
        
        form = UserChangeForm
        add_form = UserCreationForm
            
        list_display = ('nome','id','email', 'date_of_birth', 'administrador','descricao','role','telefone','foto')

        list_filter = ('is_admin', 'nome')
        fieldsets = (
            (None, {'fields': ('nome','email','password')}),
            ('Informação Pessoal', {'fields': ('date_of_birth','descricao','role','entidade','telefone','foto')}),
            ('Permissões', {'fields': ('is_admin','is_active')}),
        )

        def administrador(self, obj):
            return obj.is_admin
    
        administrador.short_description = "Administrador"

        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('nome','email','foto','date_of_birth', 'password1', 'password2','descricao','role','telefone'),
            }),
        )
        search_fields = ('nome',)
        ordering = ('nome',)
        filter_horizontal = ()

class EntidadeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class AppsTpAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id','apps','tipoPedidos')

class UserAppsAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id','usuario','app')

class StatusLogAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id','usuario','estado','dataHora')
    ordering = ('id','usuario')

class TicketAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(TicketAdmin, self).get_changeform_initial_data(request)
        get_data['id_Proprietario'] = request.user.pk
        return get_data
    
    readonly_fields = ('id',)
    list_display = ('id','nome','usuarios','estado','dataCriacao','id_Proprietario')
    ordering = ('id','usuarios')
    search_fields = ('id','usuarios','nome','id_Proprietario')
    list_filter = ('nome','usuarios','id_Proprietario')


# Registo do utilizador Admin, para fazer override do role do Django e meter o modelo de Users customizado
# no lugar dele
admin.site.register(Usuarios, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Estado)
admin.site.register(Entidades,EntidadeAdmin)
admin.site.register(Resolucao)
admin.site.register(Prioridade)
admin.site.register(TiposPedidos)
admin.site.register(Apps)
admin.site.register(Usuarios_Apps,UserAppsAdmin)
admin.site.register(Apps_tpPedidos,AppsTpAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(StatusLog,StatusLogAdmin)
