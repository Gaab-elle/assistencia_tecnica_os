<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router'; // Para redirecionar após salvar

const router = useRouter(); // Instância do router para navegação

// Dados do formulário
const ordemServico = ref({
  cliente: null,
  equipamento: null,
  tecnico_responsavel: null,
  descricao_problema: '',
  status: 'ABERTO', // Padrão ao abrir uma nova OS
  diagnostico: '',
  servico_realizado: '',
  forma_pagamento: '',
  observacoes_internas: '',
  valor_total: 0.00,
});

// Listas para dropdowns (selects)
const clientes = ref([]);
const equipamentos = ref([]);
const tecnicos = ref([]);
const erro = ref(null);
const carregando = ref(true); // Inicializado como true, pois começa carregando dados
const isEditing = ref(false); // Para saber se estamos a editar ou a criar

// Define as props que o componente pode receber (para o ID da OS em edição)
const props = defineProps({
  id: {
    type: String, // UUIDs são strings
    required: false, // Não é obrigatório para a criação (nova OS)
    default: null
  }
});


// Funções para carregar dados dos dropdowns
async function fetchClientes() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/clientes/');
    clientes.value = response.data;
  } catch (err) {
    console.error("OrdemServicoForm: Erro ao carregar clientes!", err);
    erro.value = "Erro ao carregar lista de clientes.";
  }
}

async function fetchEquipamentos() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/equipamentos/');
    equipamentos.value = response.data;
  } catch (err) {
    console.error("OrdemServicoForm: Erro ao carregar equipamentos!", err);
    erro.value = "Erro ao carregar lista de equipamentos.";
  }
}

async function fetchTecnicos() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/tecnicos/');
    tecnicos.value = response.data;
  } catch (err) {
    console.error("OrdemServicoForm: Erro ao carregar técnicos!", err);
    erro.value = "Erro ao carregar lista de técnicos.";
  }
}

// Carregar dados da OS se estiver a editar
async function fetchOsParaEdicao(osId) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/ordens-servico/${osId}/`);
    const data = response.data;

    // Mapeia os dados da API para o objeto reativo do formulário
    // Certifique-se de que os IDs são atribuídos para os v-models
    ordemServico.value = {
      cliente: data.cliente,
      equipamento: data.equipamento,
      tecnico_responsavel: data.tecnico_responsavel,
      descricao_problema: data.descricao_problema,
      status: data.status,
      diagnostico: data.diagnostico || '',
      servico_realizado: data.servico_realizado || '',
      forma_pagamento: data.forma_pagamento || '',
      observacoes_internas: data.observacoes_internas || '',
      valor_total: parseFloat(data.valor_total) || 0.00,
    };
  } catch (err) {
    console.error("OrdemServicoForm: Erro ao carregar OS para edição!", err);
    erro.value = "Erro ao carregar dados da Ordem de Serviço para edição.";
  }
}

// Função assíncrona para carregar TUDO (dropdowns e dados da OS se for edição)
async function loadAllData() {
  carregando.value = true;
  erro.value = null;
  try {
    await Promise.all([
      fetchClientes(),
      fetchEquipamentos(),
      fetchTecnicos()
    ]);

    if (props.id) { // Se um ID foi passado (modo edição)
      isEditing.value = true;
      await fetchOsParaEdicao(props.id);
    } else { // Modo criação
      isEditing.value = false;
      ordemServico.value.status = 'ABERTO'; // Garante estado inicial 'ABERTO'
    }

  } catch (e) {
    console.error("OrdemServicoForm: Erro ao carregar dados iniciais!", e);
    erro.value = "Erro fatal ao carregar dados iniciais.";
  } finally {
    carregando.value = false;
  }
}

onMounted(() => {
  loadAllData();
});

// Observa mudanças no ID da prop (útil se o componente for reutilizado na mesma rota com IDs diferentes)
watch(() => props.id, (newId) => {
  if (newId) {
    loadAllData(); // Recarrega tudo se o ID mudar
  }
});

// Função para submeter o formulário (agora para criação OU edição)
async function handleSubmit() {
  carregando.value = true; // Define carregando para true durante a submissão
  erro.value = null; // Limpa erros anteriores
  try {
    // Campos que são do modelo, incluindo os IDs das FKs.
    // Os campos `_detail` são apenas para leitura e não devem ser enviados.
    const dataToSend = {
      cliente: ordemServico.value.cliente,
      equipamento: ordemServico.value.equipamento,
      tecnico_responsavel: ordemServico.value.tecnico_responsavel,
      descricao_problema: ordemServico.value.descricao_problema,
      status: ordemServico.value.status,
      diagnostico: ordemServico.value.diagnostico,
      servico_realizado: ordemServico.value.servico_realizado,
      forma_pagamento: ordemServico.value.forma_pagamento,
      observacoes_internas: ordemServico.value.observacoes_internas,
      valor_total: ordemServico.value.valor_total,
    };

    let response;
    if (isEditing.value) {
      // Requisição PUT para atualização
      response = await axios.put(`http://127.0.0.1:8000/api/ordens-servico/${props.id}/`, dataToSend);
      alert('Ordem de Serviço atualizada com sucesso!');
    } else {
      // Requisição POST para criação
      response = await axios.post('http://127.0.0.1:8000/api/ordens-servico/', dataToSend);
      alert('Ordem de Serviço criada com sucesso!');
    }

    router.push({ name: 'os-detalhe', params: { id: response.data.id } }); // Redireciona para os detalhes da OS
  } catch (err) {
    erro.value = `Erro ao ${isEditing.value ? 'atualizar' : 'criar'} Ordem de Serviço: ` + err.message;
    if (err.response && err.response.data) {
      erro.value += ' - Detalhes: ' + JSON.stringify(err.response.data);
    }
    console.error(`Erro ao ${isEditing.value ? 'atualizar' : 'criar'} OS:`, err);
  } finally {
    carregando.value = false; // Define carregando para false após a submissão (sucesso ou falha)
  }
}
</script>

<template>
  <v-container>
    <v-card class="pa-6">
      <h2 class="text-h5 mb-4">{{ isEditing ? 'Editar Ordem de Serviço' : 'Abrir Nova Ordem de Serviço' }}</h2>
      <v-alert v-if="erro" type="error" outlined class="mb-4">{{ erro }}</v-alert>

      <div v-if="carregando" class="text-center pa-5">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-3">A carregar formulário...</p>
      </div>

      <v-form v-else-if="!carregando && !erro" @submit.prevent="handleSubmit">
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              id="cliente"
              v-model="ordemServico.cliente"
              :items="clientes"
              item-title="nome_completo"
              item-value="id"
              label="Cliente"
              :rules="[v => !!v || 'Cliente é obrigatório']"
              :disabled="isEditing"
              required
            ></v-select>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              id="equipamento"
              v-model="ordemServico.equipamento"
              :items="equipamentos"
              item-title="modelo"
              item-value="id"
              label="Equipamento"
              :rules="[v => !!v || 'Equipamento é obrigatório']"
              :disabled="isEditing"
              required
            >
              <template v-slot:item="{ item, props }">
                <v-list-item v-bind="props">
                  <v-list-item-content>
                    <v-list-item-title>{{ item.raw.marca }} {{ item.raw.modelo }}</v-list-item-title>
                    <v-list-item-subtitle>Série: {{ item.raw.numero_serie }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </template>
              <template v-slot:selection="{ item }">
                {{ item.raw.marca }} {{ item.raw.modelo }}
              </template>
            </v-select>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="6">
            <v-select
              id="tecnico"
              v-model="ordemServico.tecnico_responsavel"
              :items="tecnicos"
              item-title="usuario_username"
              item-value="usuario"
              label="Técnico Responsável"
              :rules="[v => !!v || 'Técnico é obrigatório']"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-textarea
              id="problema"
              v-model="ordemServico.descricao_problema"
              label="Descrição do Problema"
              rows="3"
              :rules="[v => !!v || 'Descrição do problema é obrigatória']"
              required
            ></v-textarea>
          </v-col>
        </v-row>

        <!-- Campos de edição (visíveis apenas no modo edição) -->
        <template v-if="isEditing">
          <v-row>
            <v-col cols="12" md="6">
              <v-textarea
                id="diagnostico"
                v-model="ordemServico.diagnostico"
                label="Diagnóstico Técnico"
                rows="3"
              ></v-textarea>
            </v-col>
            <v-col cols="12" md="6">
              <v-textarea
                id="servico_realizado"
                v-model="ordemServico.servico_realizado"
                label="Serviço Realizado"
                rows="3"
              ></v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-select
                id="status"
                v-model="ordemServico.status"
                :items="[
                  { title: 'Aberto', value: 'ABERTO' },
                  { title: 'Em Análise', value: 'EM_ANALISE' },
                  { title: 'Em Reparo', value: 'EM_REPARO' },
                  { title: 'Pronto para Retirada/Entrega', value: 'PRONTO' },
                  { title: 'Entregue', value: 'ENTREGUE' },
                  { title: 'Cancelado', value: 'CANCELADO' },
                ]"
                label="Estado"
                required
              ></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                id="valor_total"
                v-model.number="ordemServico.valor_total"
                label="Valor Total (R$)"
                type="number"
                step="0.01"
                prefix="R$"
              ></v-text-field>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                id="forma_pagamento"
                v-model="ordemServico.forma_pagamento"
                label="Forma de Pagamento"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-textarea
                id="observacoes_internas"
                v-model="ordemServico.observacoes_internas"
                label="Observações Internas"
                rows="3"
              ></v-textarea>
            </v-col>
          </v-row>
        </template>

        <v-btn type="submit" color="primary" :disabled="carregando || erro" class="mt-4">
          <v-icon left>{{ isEditing ? 'mdi-content-save' : 'mdi-plus' }}</v-icon>
          {{ carregando ? 'A guardar...' : (isEditing ? 'Atualizar Ordem de Serviço' : 'Abrir Ordem de Serviço') }}
        </v-btn>
      </v-form>
      <p v-else class="text-center text-grey">Não foi possível carregar o formulário. Verifique a consola para mais detalhes.</p>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Nenhum estilo scoped específico é necessário neste momento, o Vuetify trata da maioria. */
</style>
