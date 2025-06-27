<script setup>
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router';

const drawer = ref(true); // Controla a visibilidade da barra lateral
</script>

<template>
  <v-app color="background">
    <!-- Sidebar (v-navigation-drawer) -->
    <v-navigation-drawer app v-model="drawer" color="primary" permanent>
      <v-list-item class="pa-4">
        <v-list-item-title class="text-h6 font-weight-bold">
          YGGDRATECH

        </v-list-item-title>
        <v-list-item-subtitle>
          Menu Principal
        </v-list-item-subtitle>
      </v-list-item>

      <v-divider></v-divider>

      <v-list density="compact" nav>
          <v-list-item prepend-icon="mdi-home" title="Home" :to="{ name: 'home' }" link></v-list-item>
          <v-list-item prepend-icon="mdi-clipboard-list" title="Ordens de Serviço" :to="{ name: 'ordens-servico' }" link></v-list-item>
          <v-list-item prepend-icon="mdi-tools" title="Estoque de Peças" :to="{ name: 'pecas' }" link></v-list-item>
          <v-list-item prepend-icon="mdi-account-group" title="Clientes" :to="{ name: 'clientes-lista' }" link></v-list-item>
          <v-list-item prepend-icon="mdi-cog" title="Configurações" link></v-list-item>
        </v-list>
    </v-navigation-drawer>

    <!-- Área de Conteúdo Principal -->
    <v-main class="pa-0"> <!-- Remove padding do v-main para que o v-container interno controle -->
      <!-- O v-container aqui irá definir a largura máxima do CONTEÚDO e CENTRALIZÁ-LO -->
      <!-- class="mx-auto" centraliza horizontalmente. max-width define o limite da largura do conteúdo. -->
      <!-- pa-4 para padding interno ao container. -->
      <v-container class="pa-4 mx-auto compensar-sidebar" style="max-width: 1280px;">
        <RouterView />
      </v-container>
    </v-main>

    <!-- Rodapé -->
    <v-footer app color="primary" class="justify-center">
      <span class="white--text text-caption">&copy; {{ new Date().getFullYear() }} Assistência Técnica</span>
    </v-footer>
  </v-app>
</template>

<style>
/* Estilos globais para garantir que o scrollbar funcione corretamente */
html {
  overflow-y: auto;
  overflow-x: hidden !important; /* Esconde a barra de rolagem horizontal */
}

/* Força a cor de fundo para os elementos raiz do Vue/Vuetify */
html, body, #app {
  background-color: var(--v-theme-miceloDark-background) !important;
}

/* Ajusta o wrap para garantir que o flexbox se comporte como esperado */
.v-application__wrap {
    display: flex !important;
    flex-direction: column !important;
    width: 100vw !important;
    min-height: 100vh !important;
    background-color: var(--v-theme-miceloDark-background) !important;
}

.v-main {
  background-color: var(--v-theme-miceloDark-background) !important;
  padding: 0 !important; /* Zera padding para que o v-container interno controle */
  margin: 0 !important;
  flex-grow: 1 !important;
  display: flex;
  flex-direction: column;
}

.compensar-sidebar {
  margin-left: -20px; /* ou -24px se a sidebar tiver padding interno */
}

/* REMOVENDO AS SOBRESCRICOES GLOBAIS DE V-CONTAINER E V-COL */
/* Deixamos o v-container padrão do Vuetify lidar com isso, apenas usando as classes. */
/* Se precisar de padding customizado em colunas, use as classes pa-X diretamente na v-col. */
/* .v-container {
  max-width: none !important;
  padding-left: 16px !important;
  padding-right: 16px !important;
}
.v-col {
  padding-left: 8px !important;
  padding-right: 8px !important;
  padding-top: 8px !important;
  padding-bottom: 8px !important;
} */
</style>


