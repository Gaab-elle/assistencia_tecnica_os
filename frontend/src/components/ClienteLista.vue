<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios'; // Certifique-se de que axios está instalado (npm install axios na pasta frontend)

const clientes = ref([]);
const erro = ref(null);
const carregando = ref(true);

// Função para buscar clientes da API
async function fetchClientes() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/clientes/');
    clientes.value = response.data;
    console.log("Clientes carregados:", clientes.value);
  } catch (err) {
    erro.value = 'Erro ao carregar clientes: ' + err.message;
    console.error("Erro ao carregar clientes:", err);
  } finally {
    carregando.value = false;
  }
}

// Chama a função ao montar o componente
onMounted(() => {
  fetchClientes();
});
</script>

<template>
  <div>
    <h2>Nossos Clientes</h2>
    <p v-if="carregando">Carregando clientes...</p>
    <p v-else-if="erro" style="color: red;">{{ erro }}</p>
    <ul v-else-if="clientes.length">
      <li v-for="cliente in clientes" :key="cliente.id">
        <strong>{{ cliente.nome_completo }}</strong> - Tel: {{ cliente.telefone_principal }}
        <span v-if="cliente.email"> - Email: {{ cliente.email }}</span>
      </li>
    </ul>
    <p v-else>Nenhum cliente cadastrado.</p>
  </div>
</template>

<style scoped>
/* Estilos específicos para este componente (opcional) */
ul {
  list-style-type: none;
  padding: 0;
}
li {
  background-color: #f9f9f9;
  margin-bottom: 5px;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #eee;
}
</style>