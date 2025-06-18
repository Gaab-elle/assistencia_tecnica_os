from rest_framework import serializers
from .models import (
    Cliente,
    Equipamento,
    Tecnico,
    OrdemServico,
    PecaCategoria,
    Peca,
    ServicoPreDefinido,
    OS_Peca,
    OS_Servico
)
from django.contrib.auth.models import User


# Serializers Básicos (que não dependem de outros serializers complexos)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['id']


class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'
        read_only_fields = ['id']


class TecnicoSerializer(serializers.ModelSerializer):
    # Campo para exibir o nome de usuário do User relacionado
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Tecnico
        # Inclui o ID do usuário (FK) e o novo campo de username para exibição
        fields = ['usuario', 'usuario_username']
        read_only_fields = ['usuario']


class PecaCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PecaCategoria
        fields = '__all__'
        read_only_fields = ['id']


class PecaSerializer(serializers.ModelSerializer):
    # Para LEITURA (GET): expande os detalhes da categoria da peça
    categoria_detail = PecaCategoriaSerializer(source='categoria', read_only=True)

    # Para ESCRITA (POST/PUT): usa PrimaryKeyRelatedField para aceitar o ID da categoria
    categoria = serializers.PrimaryKeyRelatedField(queryset=PecaCategoria.objects.all())

    class Meta:
        model = Peca
        # A lista de fields é explícita para incluir tanto os campos do modelo quanto 'categoria_detail'
        fields = [
            'id', 'categoria', 'codigo_peca', 'nome_peca', 'descricao',
            'preco_custo', 'preco_venda', 'quantidade_estoque',
            'categoria_detail',
        ]
        read_only_fields = ['id']


class ServicoPreDefinidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicoPreDefinido
        fields = '__all__'
        read_only_fields = ['id']


# Serializers de Modelos Intermediários (que dependem dos Básicos)
# Eles precisam vir antes de OrdemServicoSerializer, pois OrdemServicoSerializer os utiliza.
class OS_PecaSerializer(serializers.ModelSerializer):
    # Expande os detalhes da peça para leitura
    peca_detail = PecaSerializer(source='peca', read_only=True)

    class Meta:
        model = OS_Peca
        fields = '__all__'
        read_only_fields = ['id']

    # Para escrita, o DRF precisa dos IDs da OS e da Peça
    peca = serializers.PrimaryKeyRelatedField(queryset=Peca.objects.all())
    ordem_servico = serializers.PrimaryKeyRelatedField(
        queryset=OrdemServico.objects.all())  # OrdemServico precisa ser acessível aqui (importado)


class OS_ServicoSerializer(serializers.ModelSerializer):
    # Expande os detalhes do serviço para leitura
    servico_detail = ServicoPreDefinidoSerializer(source='servico', read_only=True)

    class Meta:
        model = OS_Servico
        fields = '__all__'
        read_only_fields = ['id']

    # Para escrita, o DRF precisa dos IDs da OS e do Serviço
    servico = serializers.PrimaryKeyRelatedField(queryset=ServicoPreDefinido.objects.all())
    ordem_servico = serializers.PrimaryKeyRelatedField(
        queryset=OrdemServico.objects.all())  # OrdemServico precisa ser acessível aqui (importado)


# Serializer Principal (depende de outros Serializers)
# Este serializer deve vir POR ÚLTIMO, pois utiliza todos os serializers definidos acima.
class OrdemServicoSerializer(serializers.ModelSerializer):
    # Campos para LEITURA (GET): expandem os detalhes dos objetos relacionados (FKs diretas)
    cliente_detail = ClienteSerializer(source='cliente', read_only=True)
    equipamento_detail = EquipamentoSerializer(source='equipamento', read_only=True)
    tecnico_responsavel_detail = UserSerializer(source='tecnico_responsavel', read_only=True)

    # Campos para LEITURA (GET): expandem as listas de peças e serviços vinculados à OS (relações reversas)
    pecas_utilizadas = OS_PecaSerializer(many=True, read_only=True)
    servicos_realizados = OS_ServicoSerializer(many=True, read_only=True)

    # Campos para ESCRITA (POST/PUT): usam PrimaryKeyRelatedField para aceitar IDs.
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    equipamento = serializers.PrimaryKeyRelatedField(queryset=Equipamento.objects.all())
    tecnico_responsavel = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = OrdemServico
        # A lista 'fields' agora inclui EXPLICITAMENTE todos os campos do modelo,
        # bem como os campos '_detail' e as relações 'pecas_utilizadas'/'servicos_realizados'.
        fields = [
            'id',
            'cliente', 'equipamento', 'tecnico_responsavel',
            'cliente_detail', 'equipamento_detail', 'tecnico_responsavel_detail',
            'data_abertura', 'descricao_problema', 'status', 'diagnostico',
            'servico_realizado', 'data_fechamento', 'valor_total',
            'forma_pagamento', 'observacoes_internas',
            'pecas_utilizadas',
            'servicos_realizados',
        ]
        read_only_fields = ['id', 'data_abertura', 'data_fechamento']