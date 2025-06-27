<script setup>
import OrdemServicoForm from '@/components/OrdemServicoForm.vue';
import { useRoute } from 'vue-router'; // Para passar o ID para o formulário

const route = useRoute();
const osId = route.params.id; // Pega o ID da URL
</script>

<template>
  <main>
    <OrdemServicoForm :id="osId" />
  </main>
</template>