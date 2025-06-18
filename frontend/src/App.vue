<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>Gestão de OS</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn text :to="{ name: 'home' }">Home</v-btn>
      <v-btn text :to="{ name: 'ordens-servico' }">Ordens de Serviço</v-btn>
      <v-btn text :to="{ name: 'pecas' }">Estoque de Peças</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <RouterView />
      </v-container>
    </v-main>

    <v-footer app>
      <span>&copy; {{ new Date().getFullYear() }} Assistência Técnica</span>
    </v-footer>
  </v-app>
</template>

<style>

</style>