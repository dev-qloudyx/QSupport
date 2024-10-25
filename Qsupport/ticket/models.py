from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils import timezone
import uuid 


#Estado de cada ticket
class Estado(models.Model):
    estado = models.CharField(max_length=20)
    cor = models.CharField(max_length=30)
    font_color = models.CharField(max_length=30)
    descricao = models.CharField(max_length=300)

    def __str__(self):
        return self.estado


#Empresas cadastradas
class Entidades(models.Model):
    nome = models.CharField(max_length=100)
    externo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class MyUserManager(BaseUserManager):
    def create_user(self, nome, email, date_of_birth, password=None):
       
        if not nome:
            raise ValueError('O utilizador têm de ter um nome!')
        if not email:
            raise ValueError('O utilizador têm de ter um e-mail valido!')

        user = self.model(
            nome = nome,
            email= self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,nome, email, date_of_birth, password=None):
        user = self.create_user(
            nome = nome,
            email = self.normalize_email(email),
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#Os resposáveis na hora de contacto sobre as entidades ou podem ser operadores dependendo do "role"    
class Usuarios(AbstractBaseUser):

    uuid = models.UUIDField(default = uuid.uuid4)
    nome = models.CharField(max_length=100, unique=True,verbose_name='Utilizador')
    email = models.EmailField(verbose_name='E-mail')
    foto = models.ImageField(null=True, blank=True, upload_to='users/uploads/fotos',verbose_name='Foto')
    descricao = models.CharField(max_length=250, null=True)

    EscolhasRole = {
    ("Interno", "Interno"),
    ("Operador", "Operador"),
    ("Cliente", "Cliente"),
    }

    role = models.CharField(max_length=50,choices= EscolhasRole ,verbose_name='Cargo')
    entidade = models.ManyToManyField(Entidades, verbose_name='Entidades')
    telefone = PhoneNumberField(null=True, blank=False, unique=True, verbose_name='Telefone')
    date_of_birth = models.DateField(verbose_name='Data de Nascimento')

    is_active = models.BooleanField(default=True, verbose_name='Ativo?')
    is_admin = models.BooleanField(default=False, verbose_name='Admin?')

    objects = MyUserManager()

    USERNAME_FIELD = 'nome'
    REQUIRED_FIELDS = ['date_of_birth','email']

    def __str__(self):
        return self.nome

    def has_perm(self, perm, obj=None):
        "Permissões especificas para o utilizador"
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Membro da empresa?"
        return self.is_admin

    def nomes_entidade(self):
            return ', '.join([a.nome for a in self.entidade.all()])
    nomes_entidade.short_description = "Entidades"

class Resolucao(models.Model):
    nome = models.CharField(max_length=150)

    def __str__(self):
        return self.nome

#Classificação da prioridade do Ticket
class Prioridade(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Tipo')
    peso = models.CharField(max_length=50, verbose_name='Peso')

    def __str__(self):
        return self.nome

class TiposPedidos(models.Model):
    nome = models.CharField(max_length=100, verbose_name='Pedido')
    descricao = models.CharField(max_length=300, verbose_name='Descrição')

    def __str__(self):
        return self.nome


class Apps(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Aplicação')
    entidade = models.ForeignKey(Entidades, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True, verbose_name='Ativo?')

    def __str__(self):
        return self.nome


class Usuarios_Apps(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE,verbose_name='Utilizador')
    app = models.ForeignKey(Apps, on_delete=models.CASCADE,verbose_name='Aplicação')

    def __str__(self):
        return f"{self.app}"


class Apps_tpPedidos(models.Model):
    apps = models.ForeignKey(Apps, on_delete=models.CASCADE, verbose_name='Aplicação')
    tipoPedidos = models.ForeignKey(TiposPedidos, on_delete=models.CASCADE, verbose_name='Tipo de Pedido')

    def __str__(self):
        return f"{self.tipoPedidos}"
    

class StatusLog(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name='Estado')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, verbose_name='Utilizador')
    dataHora = models.DateTimeField(default=timezone.now(), verbose_name='Data de Criação')

    def __str__(self):
        return self.estado

    def __str__(self):
        return f"{self.estado}"

class Ticket(models.Model):
    
    uuid = models.UUIDField(default = uuid.uuid4)
    nome = models.CharField(max_length=50, verbose_name='Titulo')
    dataCriacao = models.DateTimeField(default=timezone.now(), verbose_name='Data de Criação')
    descricao = models.CharField(max_length=300, verbose_name='Descrição')
    usuarios = models.ForeignKey(Usuarios, null = True, on_delete=models.CASCADE, related_name="responsavel", verbose_name='Responsável')
    app_tpPedidos = models.ForeignKey(Apps_tpPedidos, on_delete=models.CASCADE, verbose_name='Tipo de Problema')
    prioridade = models.ForeignKey(Prioridade, null = True , on_delete=models.CASCADE, verbose_name='Prioridade')
    resolucao = models.ForeignKey(Resolucao, null = True, on_delete=models.CASCADE, verbose_name='Resolução')
    id_Proprietario = models.ForeignKey(Usuarios, null = True, on_delete=models.CASCADE, related_name="criador", verbose_name='Criador do Ticket')
    estado = models.ForeignKey(StatusLog,null = True,default = 1, on_delete=models.CASCADE, verbose_name='Estado Atual')
    usuario_app = models.ForeignKey(Usuarios_Apps,null = True, on_delete=models.CASCADE)
    app = models.ForeignKey(Apps, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Entidades_Apps(models.Model):
    entidade = models.ForeignKey(Entidades, on_delete=models.CASCADE,verbose_name='Entidade')
    app = models.ForeignKey(Apps, on_delete=models.CASCADE,verbose_name='Aplicação')

    def __str__(self):
        return f"{self.app}"

#Comentários para actualizar os avanços ou dificuldades de cada ticket
class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')
    operador = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, blank=True)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f'Comentário de {self.operador.nome} em {self.data_criacao}'
