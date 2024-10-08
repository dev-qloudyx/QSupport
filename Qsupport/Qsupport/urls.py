"""
URL configuration for Qsupport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views
from django.conf.urls.static import static
from django.conf import settings
from ticket import views as ticket_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ticket.urls')),
    path('register/', users_views.register, name ='register'), #URL para registar novos usuários
    path('login/', auth_views.LoginView.as_view(template_name ='users/login.html'), name ='login'), #URL para logar
    path('novoticket/', ticket_views.create_ticket, name ='novoticket'), #URL para criar novos tickets
    path('criar_entidades/', ticket_views.create_entidade, name ='criar_entidades'), #URL para criar novos entidades
    path('criar_app/', ticket_views.create_apps, name ='criar_app'), #URL para criar novos apps
    path('listaticket/', ticket_views.ticket_list, name ='listaticket'), #URL para a gestão de tickets
    path('listaentidades/', ticket_views.lista_entidades, name ='listaentidades'),#lista de entididades
    path('listaaplicacoes/', ticket_views.lista_apps, name ='listaaplicacoes'),#lista de aplicações
    path('listausuarios/', ticket_views.lista_user, name ='listausuarios'),#lista de usuarios
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'), #URL para o logout
    path('profile/', users_views.profile, name='profile'), #URL para os perfís
    path('<uuid:uuid>/profileedit/',users_views.editar_user, name='editar_perfil'), #URL para editar os perfis
    path('<uuid:uuid>/passwordedit/',users_views.editar_pass, name='editar_pass'), #URL para editar a password do Utilizador
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
