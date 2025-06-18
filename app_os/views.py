# assistencia_tecnica_os/app_os/views.py
from rest_framework import viewsets
# Importe todos os modelos necessários
from .models import (
    Cliente, Equipamento, Tecnico, OrdemServico,
    PecaCategoria, Peca, ServicoPreDefinido,
    OS_Peca, OS_Servico, User # User do Django para Tecnico e OrdemServico
)
# Importe todos os serializers que você criou
from .serializers import (
    ClienteSerializer, EquipamentoSerializer, TecnicoSerializer, OrdemServicoSerializer,
    PecaCategoriaSerializer, PecaSerializer, ServicoPreDefinidoSerializer,
    OS_PecaSerializer, OS_ServicoSerializer
)

# 1. ViewSet para Cliente
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('nome_completo')
    serializer_class = ClienteSerializer

# 2. ViewSet para Equipamento
class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all().order_by('tipo_equipamento', 'marca', 'modelo')
    serializer_class = EquipamentoSerializer

# 3. ViewSet para Tecnico
# Lembre-se que Tecnico está vinculado ao User do Django.
# Para criar/atualizar um Tecnico, você precisará gerenciar o objeto User subjacente.
class TecnicoViewSet(viewsets.ModelViewSet):
    # O queryset pode ser ajustado se você quiser filtrar Users que são Técnicos.
    # Ex: queryset = Tecnico.objects.filter(usuario__is_staff=True).order_by('usuario__username')
    queryset = Tecnico.objects.all().order_by('usuario__username')
    serializer_class = TecnicoSerializer

# 4. ViewSet para OrdemServico
class OrdemServicoViewSet(viewsets.ModelViewSet):
    queryset = OrdemServico.objects.all().order_by('-data_abertura')
    serializer_class = OrdemServicoSerializer

    # Para filtros adicionais, você pode sobrescrever get_queryset
    # def get_queryset(self):
    #     queryset = OrdemServico.objects.all()
    #     status = self.request.query_params.get('status', None)
    #     if status is not None:
    #         queryset = queryset.filter(status=status)
    #     return queryset.order_by('-data_abertura')

# 5. ViewSet para PecaCategoria
class PecaCategoriaViewSet(viewsets.ModelViewSet):
    queryset = PecaCategoria.objects.all().order_by('nome_categoria')
    serializer_class = PecaCategoriaSerializer

# 6. ViewSet para Peca
class PecaViewSet(viewsets.ModelViewSet):
    queryset = Peca.objects.all().order_by('nome_peca')
    serializer_class = PecaSerializer

# 7. ViewSet para ServicoPreDefinido
class ServicoPreDefinidoViewSet(viewsets.ModelViewSet):
    queryset = ServicoPreDefinido.objects.all().order_by('nome_servico')
    serializer_class = ServicoPreDefinidoSerializer

# 8. ViewSet para OS_Peca (Itens de Peça por OS)
class OS_PecaViewSet(viewsets.ModelViewSet):
    queryset = OS_Peca.objects.all()
    serializer_class = OS_PecaSerializer

    # Exemplo de como filtrar por OS específica (se a URL fosse /api/ordens-servico/{os_id}/pecas/)
    # def get_queryset(self):
    #     queryset = OS_Peca.objects.all()
    #     os_id = self.request.query_params.get('os_id', None) # Supondo parâmetro na URL
    #     if os_id is not None:
    #         queryset = queryset.filter(ordem_servico__id=os_id)
    #     return queryset

# 9. ViewSet para OS_Servico (Itens de Serviço por OS)
class OS_ServicoViewSet(viewsets.ModelViewSet):
    queryset = OS_Servico.objects.all()
    serializer_class = OS_ServicoSerializer