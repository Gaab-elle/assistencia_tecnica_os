<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { RouterLink } from 'vue-router'; // Para links de detalhes/edição futuros

const pecas = ref([]);
const erro = ref(null);
const carregando = ref(true);

// Função para buscar todas as peças
async function fetchPecas() {
  carregando.value = true;
  erro.value = null;
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/pecas/');
    pecas.value = response.data;
    console.log("Peças carregadas:", pecas.value);
  } catch (err) {
    erro.value = 'Erro ao carregar peças: ' + err.message;
    console.error("Erro ao carregar peças:", err);
  } finally {
    carregando.value = false;
  }
}

onMounted(() => {
  fetchPecas();
});
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Gestão de Estoque de Peças</h1>
    <p class="text-subtitle-1 mb-6">Aqui você pode visualizar e gerenciar suas peças em estoque.</p>

    <!-- Botão para adicionar nova peça (futuro) - estilizado com Vuetify -->
    <v-btn color="primary" :to="{ name: 'peca-criar' }" class="mb-6">
      <v-icon left>mdi-plus</v-icon> Adicionar Nova Peça
    </v-btn>

    <div v-if="carregando" class="text-center pa-5">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p class="mt-3">Carregando peças...</p>
    </div>
    <v-alert v-else-if="erro" type="error" outlined class="mb-4">{{ erro }}</v-alert>

    <v-row v-else-if="pecas.length"> <!-- Usando v-row para o grid de cartões -->
      <v-col v-for="peca in pecas" :key="peca.id" cols="12" sm="6" md="4" lg="3">
        <v-card class="peca-item pa-4"> <!-- v-card para cada item da peça -->
          <v-card-title class="text-h6 pb-2">{{ peca.nome_peca }}</v-card-title>
          <v-card-subtitle>{{ peca.codigo_peca }}</v-card-subtitle>
          <v-divider class="my-3"></v-divider>
          <v-card-text>
            <p><strong>Categoria:</strong> {{ peca.categoria_detail ? peca.categoria_detail.nome_categoria : 'N/A' }}</p>
            <p><strong>Estoque:</strong> {{ peca.quantidade_estoque }}</p>
            <p><strong>Preço Venda:</strong> R$ {{ peca.preco_venda }}</p>
            <p v-if="peca.descricao"><strong>Descrição:</strong> {{ peca.descricao }}</p>
          </v-card-text>
          <v-card-actions>
            <!-- Futuramente: Botões de Editar/Remover -->
            <v-spacer></v-spacer>
            <v-btn color="secondary" size="small" :to="{ name: 'peca-editar', params: { id: peca.id } }">
              <v-icon left>mdi-pencil</v-icon> Editar
            </v-btn>
            <v-btn color="error" size="small" @click="removerPeca(peca.id)">
              <v-icon left>mdi-delete</v-icon> Remover
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-alert v-else type="info" outlined>Nenhuma peça encontrada no estoque.</v-alert>
  </v-container>
</template>

<style scoped>
/* Nenhum estilo scoped específico é estritamente necessário aqui, o Vuetify trata da maioria. */
/* Você pode adicionar estilos extras se quiser mais personalização além do Vuetify. */
</style>