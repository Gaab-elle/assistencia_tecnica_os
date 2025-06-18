# assistencia_tecnica_os/app_os/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, EquipamentoViewSet, TecnicoViewSet, OrdemServicoViewSet,
    PecaCategoriaViewSet, PecaViewSet, ServicoPreDefinidoViewSet,
    OS_PecaViewSet, OS_ServicoViewSet
)

# Crie um router e registre nossos ViewSets com ele.
router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'equipamentos', EquipamentoViewSet)
router.register(r'tecnicos', TecnicoViewSet)
router.register(r'ordens-servico', OrdemServicoViewSet) # Usando hífens para URLs mais amigáveis
router.register(r'categorias-peca', PecaCategoriaViewSet)
router.register(r'pecas', PecaViewSet)
router.register(r'servicos-pre-definidos', ServicoPreDefinidoViewSet)
router.register(r'os-pecas', OS_PecaViewSet) # URL para o modelo intermediário de peças na OS
router.register(r'os-servicos', OS_ServicoViewSet) # URL para o modelo intermediário de serviços na OS

# As URL patterns da API são determinadas automaticamente pelo router.
urlpatterns = [
    # Se você criou a home_view, mantenha-a aqui.
    # path('', views.home_view, name='home'),

    # Inclua todas as URLs geradas pelo router
    path('', include(router.urls)),
]