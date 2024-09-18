from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Usuarios,Estado,Entidades,Resolucao,Prioridade,TiposPedidos,Apps,Usuarios_Apps,Apps_tpPedidos,Ticket,StatusLog 

#Classes necessárias para a migração de campos customizados para os Users do Django
class AccountInline(admin.StackedInline):
    model = Usuarios
    can_delete = False
    verbose_name_plural = 'Usuarios'

class CustomUserAdmin (UserAdmin):
   inlines = (AccountInline,)

#Aqui faz-se unregister para poder introduzir o model que foi criado no models.py para aceitar campos de
#usuario customizados

admin.site.register(Usuarios)
admin.site.unregister(User)
admin.site.register(User,CustomUserAdmin)
admin.site.register(Estado)
admin.site.register(Entidades)
admin.site.register(Resolucao)
admin.site.register(Prioridade)
admin.site.register(TiposPedidos)
admin.site.register(Apps)
admin.site.register(Usuarios_Apps)
admin.site.register(Apps_tpPedidos)
admin.site.register(Ticket)
admin.site.register(StatusLog)
