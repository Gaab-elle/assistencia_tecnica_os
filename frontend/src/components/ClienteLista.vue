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
<!--  <div>-->
<!--    <h2>Nossos Clientes</h2>-->
<!--    <p v-if="carregando">Carregando clientes...</p>-->
<!--    <p v-else-if="erro" style="color: red;">{{ erro }}</p>-->
<!--    <ul v-else-if="clientes.length">-->
<!--      <li v-for="cliente in clientes" :key="cliente.id">-->
<!--        <strong>{{ cliente.nome_completo }}</strong> - Tel: {{ cliente.telefone_principal }}-->
<!--        <span v-if="cliente.email"> - Email: {{ cliente.email }}</span>-->
<!--      </li>-->
<!--    </ul>-->
<!--    <p v-else>Nenhum cliente cadastrado.</p>-->
<!--  </div>-->

  <v-row class="mb-6" justify="center"> <v-col cols="12" md="10" lg="8" class="mx-auto">
      <v-card class="pa-4 rounded-lg elevation-4" color="secondary">
          <v-card-title class="text-h5 mb-3" :class="{'text-on-secondary': $vuetify.theme.current.dark}">
            <v-icon left>mdi-account-group</v-icon> Nossos Clientes Recentes
          </v-card-title>
          <v-card-text>
            <p v-if="carregandoClientes" class="text-center">
              <v-progress-circular indeterminate color="primary"></v-progress-circular> Carregando clientes...
            </p>
            <v-alert v-else-if="erroClientes" type="error" outlined>{{ erroClientes }}</v-alert>
            <v-list v-else-if="clientes.length" color="secondary" class="rounded">
              <v-list-item
                v-for="cliente in clientes"
                :key="cliente.id"
                class="mb-1 rounded"
                color="secondary"
              >
                <v-list-item-title class="text-on-secondary">
                  {{ cliente.nome_completo }} - Tel: {{ cliente.telefone_principal }}
                </v-list-item-title>
              </v-list-item>
            </v-list>
            <v-alert v-else type="info" outlined>Nenhum cliente encontrado.</v-alert>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="info" :to="{ name: 'ordens-servico' }">
              <v-icon left>mdi-clipboard-list</v-icon> Ver Todas as OSs
            </v-btn>
            <v-btn color="info" :to="{ name: 'pecas' }">
              <v-icon left>mdi-wrench</v-icon> Ver Estoque
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
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