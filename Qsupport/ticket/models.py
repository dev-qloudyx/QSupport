from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
class Estado(models.Model):
    estado = models.CharField(max_length=20)
    cor = models.CharField(max_length=30)
    font_color = models.CharField(max_length=30)
    descricao = models.CharField(max_length=300)

class Entidades(models.Model):
    nome = models.CharField(max_length=100)
    externo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Usuarios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    foto = models.ImageField(null=True, blank=True)
    descricao = models.CharField(max_length=250, null=True)
    ativo = models.BooleanField(default=True)
    role = models.CharField(max_length=50)
    entidade = models.ForeignKey(Entidades, on_delete=models.CASCADE)
    telefone = PhoneNumberField(null=False, blank=False, unique=True)
    
    def __str__(self):
        return self.user.username
    
    #Utilizado para ir buscar o id do User base para poder ir buscar mais tarde se necessário
    #Returnando o id se o user existir, ou nada se não.

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
class Resolucao(models.Model):
    nome = models.CharField(max_length=150)

class Prioridade(models.Model):
    nome = models.CharField(max_length=100)
    peso = models.CharField(max_length=50)

class TiposPedidos(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=300)

class Apps(models.Model):
    nome = models.CharField(max_length=150)
    ativo = models.BooleanField(default=True)

class Usuarios_Apps(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)

class Apps_tpPedidos(models.Model):
    apps = models.ForeignKey(Apps, on_delete=models.CASCADE)
    tipoPedidos = models.ForeignKey(TiposPedidos, on_delete=models.CASCADE)

class Ticket(models.Model):
    nome = models.CharField(max_length=50)
    dataCriacao = models.DateTimeField()
    descricao = models.CharField(max_length=300)
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    app_tpPedidos = models.ForeignKey(Apps_tpPedidos, on_delete=models.CASCADE)
    prioridade = models.ForeignKey(Prioridade, on_delete=models.CASCADE)
    resolucao = models.ForeignKey(Resolucao, on_delete=models.CASCADE)
    id_Proprietario = models.IntegerField()

class StatusLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    dataHora = models.DateTimeField()
