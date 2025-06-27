<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router'; // Importe RouterLink aqui, se ainda não estiver
import axios from 'axios';

const ordensServico = ref([]);
const erro = ref(null);
const carregando = ref(true); // O estado inicial é carregando

console.log("OrdemServicoLista: Componente inicializando."); // Log 1

// Função para buscar ordens de serviço da API
async function fetchOrdensServico() {
  console.log("OrdemServicoLista: Buscando ordens de serviço..."); // Log 2
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/ordens-servico/');
    ordensServico.value = response.data;
    console.log("OrdemServicoLista: Ordens de Serviço carregadas.", ordensServico.value.length); // Log 3
  } catch (err) {
    erro.value = 'Erro ao carregar Ordens de Serviço: ' + err.message;
    console.error("OrdemServicoLista: Erro ao carregar Ordens de Serviço!", err); // Log 4
  } finally {
    carregando.value = false; // Garante que o estado de carregamento seja finalizado
    console.log("OrdemServicoLista: Carregamento finalizado. Carregando:", carregando.value); // Log 5
  }
}

// Chama a função ao montar o componente
onMounted(() => {
  console.log("OrdemServicoLista: Componente montado. Disparando fetchOrdensServico."); // Log 6
  fetchOrdensServico();
});
</script>

<template>
  <div>
    <h2>Ordens de Serviço Abertas e em Andamento</h2>
    <p v-if="carregando">Carregando Ordens de Serviço...</p>
    <p v-else-if="erro" style="color: red;">{{ erro }}</p>
    <ul v-else-if="ordensServico.length">
      <li v-for="os in ordensServico" :key="os.id"
          :style="{ backgroundColor: os.status === 'ABERTO' ? '#e6ffe6' : os.status === 'EM_REPARO' ? '#ffffe6' : '#f0f0f0' }">
        <RouterLink :to="{ name: 'os-detalhe', params: { id: os.id } }" style="text-decoration: none; color: inherit;">
          <strong>OS #{{ os.id.substring(0, 8).toUpperCase() }}</strong> - {{ os.cliente_detail ? os.cliente_detail.nome_completo : 'N/A' }} - {{ os.status }}
          <p>Problema: {{ os.descricao_problema }}</p>
          <small>Abertura: {{ new Date(os.data_abertura).toLocaleString() }}</small>
        </RouterLink>
      </li>
    </ul>
    <p v-else>Nenhuma Ordem de Serviço encontrada.</p>
  </div>
</template>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin-bottom: 8px;
  padding: 12px;
  border-radius: 4px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}
</style>