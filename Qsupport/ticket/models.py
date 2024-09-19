from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



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
    
class Usuarios(AbstractBaseUser):
    nome = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    foto = models.ImageField(null=True, blank=True, upload_to='users/uploads/fotos')
    descricao = models.CharField(max_length=250, null=True)

    EscolhasRole = {
    ("QLOUDYX", "Qloudyx"),
    ("OPERADOR", "Operador"),
    ("CLIENTE", "Cliente"),
    }

    role = models.CharField(max_length=50,choices= EscolhasRole)
    entidade = models.ForeignKey(Entidades, on_delete=models.CASCADE)
    telefone = PhoneNumberField(null=True, blank=False, unique=True)
    date_of_birth = models.DateField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

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
