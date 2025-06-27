<script setup>
import OrdemServicoLista from '@/components/OrdemServicoLista.vue';
import { RouterLink } from 'vue-router'; // Importado para usar v-btn com :to
</script>

<template>
  <v-container> <h1 class="text-h4 mb-4">Gestão de Ordens de Serviço</h1> <p class="text-subtitle-1 mb-6">Aqui você pode visualizar e gerenciar todas as Ordens de Serviço.</p>

    <v-btn color="primary" :to="{ name: 'os-abrir' }" class="mb-6">
      <v-icon left>mdi-plus</v-icon> Abrir Nova OS
    </v-btn>

    <OrdemServicoLista />
  </v-container>
</template>

<style scoped>

</style>