<script setup>
import { ref, onMounted, defineProps, defineEmits } from 'vue';
import axios from 'axios';

// Define as props que este componente pode receber
const props = defineProps({
  osId: {
    type: String, // ID da Ordem de Serviço à qual a peça será vinculada
    required: true
  }
});

// Define os eventos que este componente pode emitir para o componente pai
const emit = defineEmits(['pecaAdicionada']);

// Dados do formulário
const novaPecaOs = ref({
  peca: null, // ID da peça selecionada
  quantidade_utilizada: 1,
  valor_unitario_venda: 0.00
});

const pecasDisponiveis = ref([]); // Lista de peças do estoque para o dropdown
const erro = ref(null);
const carregando = ref(true);
const submetendo = ref(false);

// Função para buscar todas as peças disponíveis no estoque
async function fetchPecasDisponiveis() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/pecas/');
    pecasDisponiveis.value = response.data;
    console.log("Peças disponíveis carregadas:", pecasDisponiveis.value);
  } catch (err) {
    console.error("Erro ao carregar peças disponíveis:", err);
    erro.value = "Erro ao carregar peças disponíveis.";
  } finally {
    carregando.value = false;
  }
}

// Preenche o valor de venda ao selecionar uma peça
function preencherValorVenda() {
  const pecaSelecionada = pecasDisponiveis.value.find(p => p.id === novaPecaOs.value.peca);
  if (pecaSelecionada) {
    novaPecaOs.value.valor_unitario_venda = parseFloat(pecaSelecionada.preco_venda);
  }
}

// Função para submeter o formulário
async function handleSubmit() {
  submetendo.value = true;
  erro.value = null;
  try {
    const dataToSend = {
      ordem_servico: props.osId,
      peca: novaPecaOs.value.peca,
      quantidade_utilizada: novaPecaOs.value.quantidade_utilizada,
      valor_unitario_venda: novaPecaOs.value.valor_unitario_venda,
    };

    const response = await axios.post('http://127.0.0.1:8000/api/os-pecas/', dataToSend);
    console.log('Peça adicionada à OS:', response.data);
    alert('Peça adicionada com sucesso!');

    emit('pecaAdicionada');

    novaPecaOs.value = { peca: null, quantidade_utilizada: 1, valor_unitario_venda: 0.00 };

  } catch (err) {
    erro.value = 'Erro ao adicionar peça: ' + err.message;
    if (err.response && err.response.data) {
      erro.value += ' - Detalhes: ' + JSON.stringify(err.response.data);
    }
    console.error("Erro ao adicionar peça:", err);
  } finally {
    submetendo.value = false;
  }
}

onMounted(() => {
  fetchPecasDisponiveis();
});
</script>

<template>
  <div class="add-item-form">
    <h3>Adicionar Peça à Ordem de Serviço</h3>
    <p v-if="erro" style="color: red;">{{ erro }}</p>
    <p v-if="carregando">Carregando peças disponíveis...</p>

    <form v-else @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="peca">Peça:</label>
        <select id="peca" v-model="novaPecaOs.peca" @change="preencherValorVenda" required>
          <option :value="null" disabled>Selecione uma peça</option>
          <option v-for="p in pecasDisponiveis" :key="p.id" :value="p.id">
            {{ p.nome_peca }} (Estoque: {{ p.quantidade_estoque }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="quantidade_utilizada">Quantidade:</label>
        <input type="number" id="quantidade_utilizada" v-model.number="novaPecaOs.quantidade_utilizada" min="1" required>
      </div>

      <div class="form-group">
        <label for="valor_unitario_venda">Valor Unitário (R$):</label>
        <input type="number" id="valor_unitario_venda" v-model.number="novaPecaOs.valor_unitario_venda" step="0.01" required>
      </div>

      <button type="submit" :disabled="submetendo">
        {{ submetendo ? 'Adicionando...' : 'Adicionar Peça' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.add-item-form {
  background-color: #f0f8ff;
  padding: 20px;
  border: 1px solid #cceeff;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
h3 {
  color: #007bff;
  margin-bottom: 15px;
}
.form-group {
  margin-bottom: 10px;
}
label {
  display: block;
  margin-bottom: 4px;
  font-weight: bold;
  font-size: 0.9em;
}
input[type="number"], select {
  width: 100%;
  padding: 8px;
  border: 1px solid #b3e0ff;
  border-radius: 4px;
}
button {
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1em;
  margin-top: 10px;
}
button:hover:not(:disabled) {
  background-color: #0056b3;
}
button:disabled {
  background-color: #a0a0a0;
  cursor: not-allowed;
}
</style>