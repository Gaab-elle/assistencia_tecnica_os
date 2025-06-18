<!-- assistencia_tecnica_os/frontend/src/components/PecaForm.vue -->
<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();

const props = defineProps({
  id: { // ID da peça, se estiver no modo edição
    type: String,
    required: false,
    default: null
  }
});

const peca = ref({
  categoria: null,
  codigo_peca: '',
  nome_peca: '',
  descricao: '',
  preco_custo: 0.00,
  preco_venda: 0.00,
  quantidade_estoque: 0,
});

const categorias = ref([]);
const erro = ref(null);
const carregando = ref(true);
const isEditing = ref(false);

// Funções de carregamento de dados
async function fetchCategorias() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/categorias-peca/');
    categorias.value = response.data;
  } catch (err) {
    console.error("Erro ao carregar categorias:", err);
    erro.value = "Erro ao carregar categorias de peças.";
  }
}

async function fetchPecaParaEdicao(pecaId) {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/pecas/${pecaId}/`);
    const data = response.data;
    peca.value = {
      categoria: data.categoria, // ID da categoria
      codigo_peca: data.codigo_peca,
      nome_peca: data.nome_peca,
      descricao: data.descricao || '',
      preco_custo: parseFloat(data.preco_custo),
      preco_venda: parseFloat(data.preco_venda),
      quantidade_estoque: data.quantidade_estoque,
    };
  } catch (err) {
    console.error("Erro ao carregar peça para edição:", err);
    erro.value = "Erro ao carregar dados da peça para edição.";
  }
}

// Carregamento inicial
async function loadAllData() {
  carregando.value = true;
  erro.value = null;
  try {
    await fetchCategorias(); // Carrega categorias primeiro

    if (props.id) { // Se ID existe, estamos editando
      isEditing.value = true;
      await fetchPecaParaEdicao(props.id);
    } else { // Modo criação
      isEditing.value = false;
      // Resetar formulário para valores padrão se for criação
      peca.value = {
        categoria: null,
        codigo_peca: '',
        nome_peca: '',
        descricao: '',
        preco_custo: 0.00,
        preco_venda: 0.00,
        quantidade_estoque: 0,
      };
    }
  } catch (e) {
    console.error("Erro ao carregar dados iniciais do formulário de peça:", e);
    erro.value = "Erro fatal ao carregar dados iniciais do formulário.";
  } finally {
    carregando.value = false;
  }
}

onMounted(() => {
  loadAllData();
});

watch(() => props.id, (newId) => {
  if (newId) {
    loadAllData();
  }
});

// Lógica de submissão do formulário
async function handleSubmit() {
  carregando.value = true;
  erro.value = null;
  try {
    const dataToSend = {
      ...peca.value,
      categoria: peca.value.categoria,
    };

    let response;
    if (isEditing.value) {
      response = await axios.put(`http://127.0.0.1:8000/api/pecas/${props.id}/`, dataToSend);
      alert('Peça atualizada com sucesso!');
    } else {
      response = await axios.post('http://127.0.0.1:8000/api/pecas/', dataToSend);
      alert('Peça adicionada com sucesso!');
    }
    router.push({ name: 'pecas' }); // Redireciona de volta para a lista de peças
  } catch (err) {
    erro.value = `Erro ao ${isEditing.value ? 'atualizar' : 'adicionar'} peça: ` + err.message;
    if (err.response && err.response.data) {
      erro.value += ' - Detalhes: ' + JSON.stringify(err.response.data);
    }
    console.error(`Erro ao ${isEditing.value ? 'atualizar' : 'adicionar'} peça:`, err);
  } finally {
    carregando.value = false;
  }
}
</script>

<template>
  <v-container>
    <v-card class="pa-6">
      <h2 class="text-h5 mb-4">{{ isEditing ? 'Editar Peça' : 'Adicionar Nova Peça' }}</h2>
      <v-alert v-if="erro" type="error" outlined class="mb-4">{{ erro }}</v-alert>

      <div v-if="carregando" class="text-center pa-5">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
        <p class="mt-3">Carregando formulário...</p>
      </div>

      <v-form v-else @submit.prevent="handleSubmit">
        <v-row>
          <v-col cols="12" md="6">
            <v-select
              id="categoria"
              v-model="peca.categoria"
              :items="categorias"
              item-title="nome_categoria"
              item-value="id"
              label="Categoria"
              :rules="[v => !!v || 'Categoria é obrigatória']"
              required
            ></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              id="codigo_peca"
              v-model="peca.codigo_peca"
              label="Código da Peça"
              :rules="[v => !!v || 'Código da peça é obrigatório']"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-text-field
              id="nome_peca"
              v-model="peca.nome_peca"
              label="Nome da Peça"
              :rules="[v => !!v || 'Nome da peça é obrigatório']"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12">
            <v-textarea
              id="descricao"
              v-model="peca.descricao"
              label="Descrição (opcional)"
              rows="3"
            ></v-textarea>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" md="4">
            <v-text-field
              id="preco_custo"
              v-model.number="peca.preco_custo"
              label="Preço de Custo (R$)"
              type="number"
              step="0.01"
              prefix="R$"
              :rules="[v => v >= 0 || 'Preço de custo não pode ser negativo']"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              id="preco_venda"
              v-model.number="peca.preco_venda"
              label="Preço de Venda (R$)"
              type="number"
              step="0.01"
              prefix="R$"
              :rules="[v => v >= 0 || 'Preço de venda não pode ser negativo']"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              id="quantidade_estoque"
              v-model.number="peca.quantidade_estoque"
              label="Quantidade em Estoque"
              type="number"
              min="0"
              :rules="[v => v >= 0 || 'Estoque não pode ser negativo']"
              required
            ></v-text-field>
          </v-col>
        </v-row>

        <v-btn type="submit" color="primary" :disabled="carregando || erro" class="mt-4">
          <v-icon left>{{ isEditing ? 'mdi-content-save' : 'mdi-plus' }}</v-icon>
          {{ carregando ? 'A guardar...' : (isEditing ? 'Atualizar Peça' : 'Adicionar Peça') }}
        </v-btn>
      </v-form>
      <p v-else class="text-center text-grey">Não foi possível carregar o formulário. Verifique a consola para mais detalhes.</p>
    </v-card>
  </v-container>
</template>

<style scoped>
/* Nenhum estilo scoped específico é necessário aqui. O Vuetify cuida da maioria. */
</style>