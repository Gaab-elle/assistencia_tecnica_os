<script setup>
import { ref, onMounted, defineProps, defineEmits } from 'vue';
import axios from 'axios';

// Define as props que este componente pode receber
const props = defineProps({
  osId: {
    type: String, // ID da Ordem de Serviço à qual o serviço será vinculado
    required: true
  }
});

// Define os eventos que este componente pode emitir para o componente pai
const emit = defineEmits(['servicoAdicionado']);

// Dados do formulário
const novoServicoOs = ref({
  servico: null, // ID do serviço selecionado
  preco_cobrado: 0.00
});

const servicosDisponiveis = ref([]); // Lista de serviços pré-definidos para o dropdown
const erro = ref(null);
const carregando = ref(true);
const submetendo = ref(false);

// Função para buscar todos os serviços pré-definidos
async function fetchServicosDisponiveis() {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/servicos-pre-definidos/');
    servicosDisponiveis.value = response.data;
    console.log("Serviços disponíveis carregados:", servicosDisponiveis.value);
  } catch (err) {
    console.error("Erro ao carregar serviços disponíveis:", err);
    erro.value = "Erro ao carregar serviços disponíveis.";
  } finally {
    carregando.value = false;
  }
}

// Preenche o preço cobrado ao selecionar um serviço
function preencherPrecoServico() {
  const servicoSelecionado = servicosDisponiveis.value.find(s => s.id === novoServicoOs.value.servico);
  if (servicoSelecionado) {
    novoServicoOs.value.preco_cobrado = parseFloat(servicoSelecionado.preco_fixo);
  }
}

// Função para submeter o formulário
async function handleSubmit() {
  submetendo.value = true;
  erro.value = null;
  try {
    const dataToSend = {
      ordem_servico: props.osId, // ID da OS vindo das props
      servico: novoServicoOs.value.servico, // ID do serviço selecionado
      preco_cobrado: novoServicoOs.value.preco_cobrado,
    };

    const response = await axios.post('http://127.0.0.1:8000/api/os-servicos/', dataToSend);
    console.log('Serviço adicionado à OS:', response.data);
    alert('Serviço adicionado com sucesso!');

    // Emite um evento para o componente pai (OrdemServicoDetalhe)
    emit('servicoAdicionado');

    // Opcional: Resetar o formulário após adicionar
    novoServicoOs.value = { servico: null, preco_cobrado: 0.00 };

  } catch (err) {
    erro.value = 'Erro ao adicionar serviço: ' + err.message;
    if (err.response && err.response.data) {
      erro.value += ' - Detalhes: ' + JSON.stringify(err.response.data);
    }
    console.error("Erro ao adicionar serviço:", err);
  } finally {
    submetendo.value = false;
  }
}

onMounted(() => {
  fetchServicosDisponiveis();
});
</script>

<template>
  <div class="add-item-form">
    <h3>Adicionar Serviço à Ordem de Serviço</h3>
    <p v-if="erro" style="color: red;">{{ erro }}</p>
    <p v-if="carregando">Carregando serviços disponíveis...</p>

    <form v-else @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="servico">Serviço:</label>
        <select id="servico" v-model="novoServicoOs.servico" @change="preencherPrecoServico" required>
          <option :value="null" disabled>Selecione um serviço</option>
          <option v-for="s in servicosDisponiveis" :key="s.id" :value="s.id">
            {{ s.nome_servico }} (R$ {{ s.preco_fixo }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="preco_cobrado">Preço Cobrado (R$):</label>
        <input type="number" id="preco_cobrado" v-model.number="novoServicoOs.preco_cobrado" step="0.01" min="0" required>
      </div>

      <button type="submit" :disabled="submetendo">
        {{ submetendo ? 'Adicionando...' : 'Adicionar Serviço' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.add-item-form {
  background-color: #e6f7ff; /* Cor levemente diferente para distinguir */
  padding: 20px;
  border: 1px solid #b3e0ff;
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
  border: 1px solid #99d6ff;
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