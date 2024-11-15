from django import forms
from django.contrib import admin
from django.contrib.auth.models import User,Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import Usuarios,Estado,Entidades,Resolucao,Prioridade,TiposPedidos,Apps,Usuarios_Apps,Apps_tpPedidos,Ticket,StatusLog,Entidades_Apps,AcaoEstado,Comentario
class UserChangeForm(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = Usuarios
        fields = ('nome','email', 'password','descricao','date_of_birth','is_active','is_admin')


class UserAdmin(BaseUserAdmin):
    
        form = UserChangeForm
        #add_form = UserCreationForm

        list_display = ('nome','uuid','id','nomes_entidade','email', 'date_of_birth', 'administrador','descricao','role','telefone','foto')

        list_filter = ('is_admin', 'nome')
        fieldsets = (
            (None, {'fields': ('nome','email','password')}),
            ('Informação Pessoal', {'fields': ('date_of_birth','descricao','role','entidade','telefone','foto')}),
            ('Permissões',{'fields': ('is_admin','is_active','uuid')}),
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

class PrioridadeAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class EstadoAdmin(admin.ModelAdmin):
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
    list_display = ('id','uuid','nome','usuarios','estado','dataCriacao','dataAtualizacao','id_Proprietario','url',)
    ordering = ('id','usuarios')
    search_fields = ('id','usuarios','nome','id_Proprietario')
    list_filter = ('nome','usuarios','id_Proprietario')


# Registo do utilizador Admin, para fazer override do role do Django e meter o modelo de Users customizado
# no lugar dele
admin.site.register(Usuarios, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Estado, EstadoAdmin)
admin.site.register(Entidades,EntidadeAdmin)
admin.site.register(Resolucao)
admin.site.register(Prioridade, PrioridadeAdmin)
admin.site.register(TiposPedidos)
admin.site.register(Apps)
admin.site.register(Usuarios_Apps,UserAppsAdmin)
admin.site.register(Apps_tpPedidos,AppsTpAdmin)
admin.site.register(Ticket,TicketAdmin)
admin.site.register(StatusLog,StatusLogAdmin)
admin.site.register(Entidades_Apps)
admin.site.register(AcaoEstado)
admin.site.register(Comentario)