<script setup>
import ClienteLista from '@/components/ClienteLista.vue';
import HelloWorld from '@/components/HelloWorld.vue'; // Mantenha se você ainda tem HelloWorld.vue

// REMOVA ESTA LINHA: import TheWelcome from '@/components/TheWelcome.vue';

// Note: ClienteLista já carrega os clientes dentro dele
</script>

<template>
  <main>
    <HelloWorld msg="Bem-vindo ao seu sistema de OS!" />

    <hr style="margin-top: 20px; margin-bottom: 20px;">

    <ClienteLista />

  </main>
</template>

<style scoped>
/* Estilos específicos para HomeView.vue */
.wrapper {
  display: flex;
  place-items: flex-start;
  flex-wrap: wrap;
}
</style>