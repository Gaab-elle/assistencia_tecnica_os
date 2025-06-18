# assistencia_tecnica_os/app_os/admin.py
from django.contrib import admin
from .models import (
    Cliente, Equipamento, Tecnico, OrdemServico,
    PecaCategoria, Peca, ServicoPreDefinido,
    OS_Peca, OS_Servico
)

# Registre seus modelos aqui
admin.site.register(Cliente)
admin.site.register(Equipamento)
admin.site.register(Tecnico)
admin.site.register(OrdemServico)
admin.site.register(PecaCategoria)
admin.site.register(Peca)
admin.site.register(ServicoPreDefinido)
admin.site.register(OS_Peca)
admin.site.register(OS_Servico)
