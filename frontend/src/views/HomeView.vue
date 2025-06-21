<script setup>
import ClienteLista from '@/components/ClienteLista.vue';
</script>

<template>
  <!-- Conteúdo da HomeView.vue diretamente dentro do v-container fluido de App.vue -->
  <div>
    <v-row class="text-center my-5">
      <v-col cols="12">
        <h1 class="text-h3 font-weight-bold mb-4" :class="{'text-on-background': $vuetify.theme.current.dark}">
          Bem-vindo ao seu Sistema de Gestão de OS!
        </h1>
        <p class="text-subtitle-1 text-medium-emphasis" :class="{'text-on-background': $vuetify.theme.current.dark}">
          A sua solução completa para gerenciar ordens de serviço, clientes, estoque de peças e técnicos.
        </p>
      </v-col>
    </v-row>

    <v-divider class="my-5"></v-divider>

    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="pa-4" color="secondary"> <!-- Usando color="secondary" para o fundo do card -->
          <v-card-title class="text-h5 mb-3" :class="{'text-on-secondary': $vuetify.theme.current.dark}">
            <v-icon left>mdi-account-group</v-icon> Nossos Clientes Recentes
          </v-card-title>
          <v-card-text>
            <ClienteLista />
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
  </div>
</template>

<style scoped>
/* Nenhum estilo scoped adicional necessário. */
</style>
