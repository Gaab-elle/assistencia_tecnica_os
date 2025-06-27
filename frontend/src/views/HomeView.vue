<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ClienteLista from '@/components/ClienteLista.vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const clientes = ref([]);
const erroClientes = ref(null);
const carregandoClientes = ref(true);

const cardData = ref([
  { title: 'Vendidas', value: 11, priority: 'Baixa', color: '#FF9800', icon: 'mdi-currency-usd' },
  { title: 'Hoje', value: 0, priority: 'Normal', color: '#2196F3', icon: 'mdi-calendar-today' },
  { title: 'Amanhã', value: 3, priority: 'Normal', color: '#4CAF50', icon: 'mdi-calendar-arrow-right' },
  { title: 'No prazo', value: 131, priority: 'Alta', color: '#9C27B0', icon: 'mdi-check-circle' },
  { title: 'Atrasado', value: 23, priority: 'Alta', color: '#F44336', icon: 'mdi-alert-circle' },
  { title: 'Baixa', value: 113, priority: 'Baixa', color: '#00BCD4', icon: 'mdi-arrow-down' },
]);

const situationData = ref([
  { title: 'Enviar p/ Cliente', value: 8 },
  { title: 'Aguar. Resposta', value: 6 },
  { title: 'Comprar Peça', value: 6 },
  { title: 'Aguar. Peça', value: 9 },
  { title: 'Testes Finais', value: 5 },
  { title: 'Postar Correios', value: 2 },
  { title: 'Entregar p/ Cliente', value: 89 },
]);

const chartData = ref({
  labels: ['Orçamento', 'Aberto', 'Andamento', 'Pausado', 'Concluído', 'Finalizado', 'Cancelado'],
  datasets: [
    {
      label: 'Estatísticas de OS',
      backgroundColor: ['#FF9800', '#2196F3', '#4CAF50', '#FFEB3B', '#9C27B0', '#F44336', '#00BCD4'],
      data: [45, 60, 50, 10, 80, 30, 5]
    }
  ]
});

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: { color: '#E0E0E0' },
      grid: { color: 'rgba(255,255,255,0.1)' }
    },
    x: {
      ticks: { color: '#E0E0E0' },
      grid: { color: 'rgba(255,255,255,0.05)' }
    }
  },
  plugins: {
    legend: {
      labels: { color: '#E0E0E0' }
    }
  }
});

async function fetchClientes() {
  carregandoClientes.value = true;
  erroClientes.value = null;
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/clientes/');
    clientes.value = response.data;
  } catch (err) {
    erroClientes.value = 'Erro ao carregar clientes: ' + err.message;
    console.error("Erro ao carregar clientes:", err);
  } finally {
    carregandoClientes.value = false;
  }
}

onMounted(() => {
  fetchClientes();
});
</script>

<template>
<v-container class="ml-auto mr-auto px-4" style="max-width: 1000px;">
    <v-row class="text-center my-5" justify="center">
      <v-col cols="8" class="mx-auto text-center">
        <h1 class="text-h3 font-weight-bold mb-4" :class="{ 'text-on-background': $vuetify.theme.current.dark }">
          Bem-vindo ao seu Sistema de Gestão de OS!
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis" :class="{ 'text-on-background': $vuetify.theme.current.dark }">
          A sua solução completa para gerenciar ordens de serviço, clientes, estoque de peças e técnicos.
        </p>
      </v-col>
    </v-row>

    <v-divider class="my-5"></v-divider>

    <!-- Cards de estatística centralizados -->
    <v-container fluid>
      <v-row class="mb-4" justify="center">
        <v-col
          v-for="(card, index) in cardData"
          :key="index"
          cols="6"
          sm="4"
          md="2"
          lg="2"
          class="d-flex justify-center"
        >
          <v-card :color="card.color" class="text-center rounded-lg elevation-2 card-estatistica">
            <v-icon size="24" class="icon-spacing text-white">{{ card.icon }}</v-icon>
            <v-card-title class="font-weight-bold text-white card-value-text pa-0">{{ card.value }}</v-card-title>
            <v-card-subtitle class="text-white text-caption card-title-text pa-0">{{ card.title }}</v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Situação -->
    <v-row class="mb-4" justify="center">
      <v-col cols="8">
        <v-card color="secondary" class="pa-1 text-center rounded-sl elevation-4 ma-0_5">
          <v-card-title class="text-h6 text-on-secondary">Situação</v-card-title>
          <v-divider class="my-3"></v-divider>
          <v-row dense justify="center" class="flex-wrap">
            <v-col v-for="(item, index) in situationData" :key="index" cols="auto" class="flex-grow-0 flex-shrink-0">
              <v-card color="surface" class="pa-2 text-center rounded-lg elevation-0 custom-situation-card">
                <v-card-title class="text-h6 font-weight-bold text-on-surface mb-0 pa-0">
                  {{ item.value }}
                </v-card-title>
                <v-card-subtitle class="text-on-surface text-caption pa-0">
                  {{ item.title }}
                </v-card-subtitle>
              </v-card>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>

    <!-- Gráfico -->
    <v-row class="mb-6 mt-12 my-5" justify="center">
      <v-col cols="8">
        <v-card color="secondary" class="pa-1 text-center rounded-lg elevation-4 ma-0_5">
          <v-card-title class="text-h6 text-on-secondary">Estatísticas de OS</v-card-title>
          <v-card-text>
            <Bar :data="chartData" :options="chartOptions" style="height: 300px;" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.card-estatistica {
  max-width: 140px;
  width: 100%;
  min-height: 90px !important;
  height: auto !important;
  padding: 8px 4px !important;
  margin: 6px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-left: auto;
  margin-right: auto;
}

.custom-situation-card {
  min-width: 90px;
  max-width: 120px;
  margin: 0 6px;
  padding: 8px 10px !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.custom-situation-card .v-card-title {
  font-size: 1.2rem !important;
  line-height: 1.2 !important;
}

.custom-subtitle-situation {
  font-size: 0.75rem !important;
  line-height: 1.1 !important;
  white-space: normal;
  overflow: visible;
  text-overflow: clip;
  max-width: 100%;
}

.v-list-item .text-on-secondary {
  font-size: 0.85em !important;
}

.pa-0_5 {
  padding: 2px !important;
}
</style>
