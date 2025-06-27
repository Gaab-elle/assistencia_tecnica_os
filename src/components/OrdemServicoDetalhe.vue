<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import axios from 'axios';
import OS_PecaAddForm from './OS_PecaAddForm.vue';   // Importa o componente do formulário de adição de peças
import OS_ServicoAddForm from '@/components/OS_ServicoAddForm.vue'; // Importa o componente do formulário de adição de serviços

const route = useRoute(); // Obtém o objeto de rota atual
const osId = ref(null);   // Para armazenar o ID da OS da URL
const osDetalhes = ref(null);
const erro = ref(null);
const carregando = ref(true);
const removendoItem = ref(false); // Estado para desabilitar botões durante a remoção

// Função para buscar os detalhes de uma OS específica
async function fetchOsDetalhes(id) {
  carregando.value = true;
  erro.value = null;
  osDetalhes.value = null; // Limpa os detalhes anteriores
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/ordens-servico/${id}/`);
    osDetalhes.value = response.data;
    console.log("Detalhes da OS carregados:", osDetalhes.value);
  } catch (err) {
    if (err.response && err.response.status === 404) {
      erro.value = 'Ordem de Serviço não encontrada.';
    } else {
      erro.value = 'Erro ao carregar detalhes da OS: ' + err.message;
    }
    console.error("Erro ao carregar detalhes da OS:", err);
  } finally {
    carregando.value = false;
  }
}

// Função para recarregar os detalhes da OS (útil após adicionar/remover itens)
function refreshOsDetails() {
  fetchOsDetalhes(osId.value);
}

// FUNÇÃO: Remover Peça da OS
async function removerPeca(osPecaId) {
  if (!confirm('Tem certeza que deseja remover esta peça da OS?')) {
    return; // Cancela se o utilizador não confirmar
  }
  removendoItem.value = true; // Ativa o estado de remoção (para desabilitar botões)
  try {
    await axios.delete(`http://127.0.0.1:8000/api/os-pecas/${osPecaId}/`);
    alert('Peça removida com sucesso!');
    refreshOsDetails(); // Recarrega os detalhes da OS para atualizar a lista
  } catch (err) {
    console.error("Erro ao remover peça:", err);
    erro.value = 'Erro ao remover peça: ' + err.message;
  } finally {
    removendoItem.value = false; // Desativa o estado de remoção
  }
}

// FUNÇÃO: Remover Serviço da OS
async function removerServico(osServicoId) {
  if (!confirm('Tem certeza que deseja remover este serviço da OS?')) {
    return; // Cancela se o utilizador não confirmar
  }
  removendoItem.value = true; // Ativa o estado de remoção
  try {
    await axios.delete(`http://127.0.0.1:8000/api/os-servicos/${osServicoId}/`);
    alert('Serviço removido com sucesso!');
    refreshOsDetails(); // Recarrega os detalhes da OS para atualizar a lista
  } catch (err) {
    console.error("Erro ao remover serviço:", err);
    erro.value = 'Erro ao remover serviço: ' + err.message;
  } finally {
    removendoItem.value = false; // Desativa o estado de remoção
  }
}

// Observa mudanças no parâmetro 'id' da rota (útil se o componente for reutilizado na mesma rota)
watch(() => route.params.id, (newId) => {
  osId.value = newId;
  if (newId) {
    fetchOsDetalhes(newId);
  }
}, { immediate: true }); // 'immediate: true' faz com que a função seja executada na montagem inicial também

// Chamada inicial quando o componente é montado
onMounted(() => {
  osId.value = route.params.id;
  if (osId.value) {
    fetchOsDetalhes(osId.value);
  }
});
</script>

<template>
  <v-container> <!-- Usa v-container para alinhar o conteúdo -->
    <v-card v-if="carregando" class="pa-5 text-center" flat>
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">A carregar detalhes da Ordem de Serviço...</p>
    </v-card>
    <v-alert v-else-if="erro" type="error" outlined class="mb-4">{{ erro }}</v-alert>

    <v-card v-else-if="osDetalhes" class="pa-6"> <!-- Usa v-card para o contentor principal -->
      <h2 class="text-h5 mb-4">Detalhes da Ordem de Serviço #{{ osDetalhes.id.substring(0, 8).toUpperCase() }}</h2>

      <!-- Botão de Editar -->
      <v-btn color="secondary" :to="{ name: 'os-editar', params: { id: osDetalhes.id } }" class="mb-4">
        <v-icon left>mdi-pencil</v-icon> Editar OS
      </v-btn>

      <v-divider class="my-4"></v-divider>

      <v-row class="mb-2">
        <v-col cols="12" sm="6">
          <p class="text-subtitle-1"><strong>Estado:</strong>
            <v-chip :color="osDetalhes.status === 'ABERTO' ? 'green' : osDetalhes.status === 'EM_REPARO' ? 'amber' : 'grey'" size="small">{{ osDetalhes.status }}</v-chip>
          </p>
        </v-col>
        <v-col cols="12" sm="6">
          <p class="text-subtitle-1"><strong>Data de Abertura:</strong> {{ new Date(osDetalhes.data_abertura).toLocaleString() }}</p>
        </v-col>
      </v-row>

      <v-row class="mb-2">
        <v-col cols="12" md="6">
          <p class="text-subtitle-1"><strong>Cliente:</strong> {{ osDetalhes.cliente_detail ? osDetalhes.cliente_detail.nome_completo : 'N/A' }}</p>
        </v-col>
        <v-col cols="12" md="6">
          <p class="text-subtitle-1"><strong>Equipamento:</strong> {{ osDetalhes.equipamento_detail ? osDetalhes.equipamento_detail.marca + ' ' + osDetalhes.equipamento_detail.modelo : 'N/A' }} (Série: {{ osDetalhes.equipamento_detail ? osDetalhes.equipamento_detail.numero_serie : 'N/A' }})</p>
        </v-col>
      </v-row>
      <p class="text-subtitle-1 mb-4"><strong>Técnico Responsável:</strong> {{ osDetalhes.tecnico_responsavel_detail ? osDetalhes.tecnico_responsavel_detail.username : 'N/A' }}</p>

      <h3 class="text-h6 mt-6 mb-3">Problema e Diagnóstico:</h3>
      <p class="mb-2"><strong>Problema Relatado:</strong> {{ osDetalhes.descricao_problema }}</p>
      <p v-if="osDetalhes.diagnostico" class="mb-2"><strong>Diagnóstico:</strong> {{ osDetalhes.diagnostico }}</p>
      <p v-if="osDetalhes.servico_realizado" class="mb-4"><strong>Serviço Realizado:</strong> {{ osDetalhes.servico_realizado }}</p>

      <v-divider class="my-4"></v-divider>

      <h3 class="text-h6 mt-6 mb-3">Peças Utilizadas:</h3>
      <v-list v-if="osDetalhes.pecas_utilizadas && osDetalhes.pecas_utilizadas.length" dense>
        <v-list-item v-for="itemPeca in osDetalhes.pecas_utilizadas" :key="itemPeca.id">
          <v-list-item-content>
            <v-list-item-title>
              {{ itemPeca.quantidade_utilizada }}x {{ itemPeca.peca_detail ? itemPeca.peca_detail.nome_peca : 'Peça Desconhecida' }}
            </v-list-item-title>
            <v-list-item-subtitle>
              R$ {{ itemPeca.valor_unitario_venda }}
            </v-list-item-subtitle>
          </v-list-item-content>
          <template v-slot:append>
            <v-btn icon color="error" size="small" @click="removerPeca(itemPeca.id)" :disabled="removendoItem">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-list-item>
      </v-list>
      <p v-else class="text-body-2 text-grey">Nenhuma peça utilizada nesta OS.</p>

      <h3 class="text-h6 mt-6 mb-3">Serviços Realizados:</h3>
      <v-list v-if="osDetalhes.servicos_realizados && osDetalhes.servicos_realizados.length" dense>
        <v-list-item v-for="itemServico in osDetalhes.servicos_realizados" :key="itemServico.id">
          <v-list-item-content>
            <v-list-item-title>
              {{ itemServico.servico_detail ? itemServico.servico_detail.nome_servico : 'Serviço Desconhecido' }}
            </v-list-item-title>
            <v-list-item-subtitle>
              R$ {{ itemServico.preco_cobrado }}
            </v-list-item-subtitle>
          </v-list-item-content>
          <template v-slot:append>
            <v-btn icon color="error" size="small" @click="removerServico(itemServico.id)" :disabled="removendoItem">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </template>
        </v-list-item>
      </v-list>
      <p v-else class="text-body-2 text-grey">Nenhum serviço realizado nesta OS.</p>

      <v-divider class="my-4"></v-divider>

      <v-row class="mt-4">
        <v-col cols="12" sm="6">
          <p class="text-h6"><strong>Valor Total:</strong> R$ {{ osDetalhes.valor_total }}</p>
        </v-col>
        <v-col cols="12" sm="6">
          <p v-if="osDetalhes.forma_pagamento" class="text-h6"><strong>Forma de Pagamento:</strong> {{ osDetalhes.forma_pagamento }}</p>
        </v-col>
      </v-row>

      <p v-if="osDetalhes.data_fechamento" class="text-subtitle-1 mt-2"><strong>Data de Fechamento:</strong> {{ new Date(osDetalhes.data_fechamento).toLocaleString() }}</p>
      <p v-if="osDetalhes.observacoes_internas" class="text-body-2 mt-2"><strong>Observações Internas:</strong> {{ osDetalhes.observacoes_internas }}</p>

      <v-divider class="my-6"></v-divider>

      <!-- Formulários de Adição de Peças e Serviços -->
      <v-row>
        <v-col cols="12" md="6">
          <OS_PecaAddForm :osId="osDetalhes.id" @pecaAdicionada="refreshOsDetails" />
        </v-col>
        <v-col cols="12" md="6">
          <OS_ServicoAddForm :osId="osDetalhes.id" @servicoAdicionado="refreshOsDetails" />
        </v-col>
      </v-row>

    </v-card>
    <v-alert v-else type="info" outlined>OS não encontrada ou a carregar...</v-alert>
  </v-container>
</template>

<style scoped>
/* Nenhum estilo personalizado é necessário neste momento, o Vuetify trata da maioria. */
/* Estilos para .btn-secondary, etc. foram removidos, pois os botões v-btn têm estilos incorporados. */
</style>
