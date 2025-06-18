import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # Necessário para o modelo Tecnico e para vincular à OrdemServico

# 1. Modelo Cliente
class Cliente(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    telefone_principal = models.CharField(max_length=20, verbose_name="Telefone Principal")
    telefone_secundario = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Telefone Secundário"
    )
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço Completo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

# 2. Modelo Equipamento
class Equipamento(models.Model):
    TIPO_EQUIPAMENTO_CHOICES = [
        ('NOTEBOOK', 'Notebook'),
        ('PC_MESA', 'PC de Mesa'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name='equipamentos',
        verbose_name="Cliente"
    )
    tipo_equipamento = models.CharField(
        max_length=10,
        choices=TIPO_EQUIPAMENTO_CHOICES,
        verbose_name="Tipo de Equipamento"
    )
    marca = models.CharField(max_length=100, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    numero_serie = models.CharField(
        max_length=100, unique=True, verbose_name="Número de Série"
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações do Equipamento")

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        ordering = ['tipo_equipamento', 'marca', 'modelo']

    def __str__(self):
        return f"{self.tipo_equipamento} {self.marca} {self.modelo} ({self.numero_serie})"

# 3. Modelo Tecnico
from django.contrib.auth.models import User # Django já possui um modelo de usuário

class Tecnico(models.Model):
    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name="Usuário do Sistema"
    )
    # Adicione campos específicos do técnico aqui, se precisar
    # exemplo: especialidade = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Técnico"
        verbose_name_plural = "Técnicos"

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username

# 4. Modelo OrdemServico
class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('EM_ANALISE', 'Em Análise'),
        ('EM_REPARO', 'Em Reparo'),
        ('PRONTO', 'Pronto para Retirada/Entrega'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='ordens_servico',
        verbose_name="Cliente"
    )
    equipamento = models.ForeignKey(
        Equipamento,
        on_delete=models.PROTECT,
        related_name='ordens_servico',
        verbose_name="Equipamento"
    )
    tecnico_responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='os_responsavel',
        verbose_name="Técnico Responsável"
    )
    data_abertura = models.DateTimeField(default=timezone.now, verbose_name="Data de Abertura")
    descricao_problema = models.TextField(verbose_name="Descrição do Problema")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ABERTO',
        verbose_name="Status da OS"
    )
    diagnostico = models.TextField(blank=True, null=True, verbose_name="Diagnóstico Técnico")
    servico_realizado = models.TextField(blank=True, null=True, verbose_name="Serviço Realizado")
    data_fechamento = models.DateTimeField(blank=True, null=True, verbose_name="Data de Fechamento")
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Total"
    )
    forma_pagamento = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Forma de Pagamento"
    )
    observacoes_internas = models.TextField(
        blank=True, null=True, verbose_name="Observações Internas"
    )

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ['-data_abertura']

    def __str__(self):
        return f"OS {str(self.id)[:8].upper()} - {self.cliente.nome_completo} - {self.status}"

    def save(self, *args, **kwargs):
        if self.status in ['ENTREGUE', 'CANCELADO'] and not self.data_fechamento:
            self.data_fechamento = timezone.now()
        elif self.status not in ['ENTREGUE', 'CANCELADO'] and self.data_fechamento:
            self.data_fechamento = None
        super().save(*args, **kwargs)

# 5. Modelo PecaCategoria
class PecaCategoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_categoria = models.CharField(
        max_length=100, unique=True, verbose_name="Nome da Categoria"
    )

    class Meta:
        verbose_name = "Categoria de Peça"
        verbose_name_plural = "Categorias de Peças"
        ordering = ['nome_categoria']

    def __str__(self):
        return self.nome_categoria

# 6. Modelo Peca
class Peca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    categoria = models.ForeignKey(
        PecaCategoria,
        on_delete=models.PROTECT,
        related_name='pecas',
        verbose_name="Categoria"
    )
    codigo_peca = models.CharField(
        max_length=50, unique=True, verbose_name="Código da Peça"
    )
    nome_peca = models.CharField(max_length=255, verbose_name="Nome da Peça")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco_custo = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço de Custo"
    )
    preco_venda = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço de Venda"
    )
    quantidade_estoque = models.IntegerField(default=0, verbose_name="Quantidade em Estoque")

    class Meta:
        verbose_name = "Peça"
        verbose_name_plural = "Peças"
        ordering = ['nome_peca']

    def __str__(self):
        return f"{self.nome_peca} ({self.codigo_peca})"

# 7. Modelo ServicoPreDefinido
class ServicoPreDefinido(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_servico = models.CharField(
        max_length=255, unique=True, verbose_name="Nome do Serviço"
    )
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição do Serviço")
    preco_fixo = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço Fixo"
    )

    class Meta:
        verbose_name = "Serviço Pré-Definido"
        verbose_name_plural = "Serviços Pré-Definidos" # Corrigido aqui
        ordering = ['nome_servico']

    def __str__(self):
        return f"{self.nome_servico} (R$ {self.preco_fixo})"

# 8. Modelo OS_Peca (Tabela de ligação para ManyToMany)
class OS_Peca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='pecas_utilizadas',
        verbose_name="Ordem de Serviço"
    )
    peca = models.ForeignKey(
        Peca,
        on_delete=models.PROTECT,
        related_name='usada_em_os',
        verbose_name="Peça"
    )
    quantidade_utilizada = models.IntegerField(default=1, verbose_name="Quantidade Utilizada")
    valor_unitario_venda = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Valor Unitário (na OS)"
    )

    class Meta:
        verbose_name = "Peça Utilizada na OS"
        verbose_name_plural = "Peças Utilizadas na OS"
        unique_together = ('ordem_servico', 'peca')

    def __str__(self):
        return f"{self.peca.nome_peca} x {self.quantidade_utilizada} na OS {str(self.ordem_servico.id)[:8].upper()}"

# 9. Modelo OS_Servico (Tabela de ligação para ManyToMany)
class OS_Servico(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name='servicos_realizados',
        verbose_name="Ordem de Serviço"
    )
    servico = models.ForeignKey(
        ServicoPreDefinido,
        on_delete=models.PROTECT,
        related_name='aplicado_em_os',
        verbose_name="Serviço"
    )
    preco_cobrado = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Preço Cobrado na OS"
    )

    class Meta:
        verbose_name = "Serviço Realizado na OS"
        verbose_name_plural = "Serviços Realizados na OS"
        unique_together = ('ordem_servico', 'servico')

    def __str__(self):
        return f"{self.servico.nome_servico} na OS {str(self.ordem_servico.id)[:8].upper()}"