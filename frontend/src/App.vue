<script setup>
// Importações necessárias do Vue e Vue Router
import { ref } from 'vue';
import { RouterLink, RouterView } from 'vue-router'; // RouterLink e RouterView são essenciais para navegação

// Variável reativa para controlar a visibilidade da barra lateral (drawer)
// Definida como true para que a barra lateral comece aberta por padrão
const drawer = ref(true);
</script>

<template>
  <!-- v-app é o componente raiz do Vuetify para toda a aplicação. -->
  <!-- A propriedade 'color="background"' aplica a cor de fundo definida no tema 'miceloDark' (App.vue) a toda a aplicação. -->
  <v-app color="background">
     <!--Componente v-navigation-drawer: É a barra lateral de navegação. -->
    <!-- 'app' posiciona-a corretamente na aplicação. -->
    <!-- 'v-model="drawer"' liga a visibilidade à variável 'drawer'. -->
    <!-- 'color="primary"' define a cor de fundo da barra lateral (o azul escuro principal do tema). -->
    <!-- 'permanent' faz com que a barra lateral esteja sempre visível em desktops. -->
    <v-navigation-drawer app v-model="drawer" color="primary" permanent>
      <!-- Conteúdo do cabeçalho da barra lateral -->
      <v-list-item class="pa-4">
        <v-list-item-title class="text-h6 font-weight-bold">
          MICLEO OS <!-- Título principal da sua aplicação -->
        </v-list-item-title>
        <v-list-item-subtitle>
          Menu Principal <!-- Subtítulo do menu -->
        </v-list-item-subtitle>
      </v-list-item>

      <!-- Divisor visual para separar o cabeçalho do menu de navegação -->
      <v-divider></v-divider>

      <!-- Lista de itens de navegação na barra lateral -->
      <!-- 'density="compact"' para tornar os itens mais compactos. -->
      <!-- 'nav' para aplicar estilos de navegação padrão do Vuetify. -->
      <v-list density="compact" nav>
        <!-- Cada v-list-item é um link de navegação. -->
        <!-- 'prepend-icon' adiciona um ícone antes do texto. -->
        <!-- 'title' define o texto do link. -->
        <!-- ':to="{ name: 'home' }"' especifica a rota para onde o link aponta. -->
        <!-- 'link' aplica os estilos de link clicável do Vuetify. -->
        <v-list-item prepend-icon="mdi-home" title="Home" :to="{ name: 'home' }" link></v-list-item>
        <v-list-item prepend-icon="mdi-clipboard-list" title="Ordens de Serviço" :to="{ name: 'ordens-servico' }" link></v-list-item>
        <v-list-item prepend-icon="mdi-tools" title="Estoque de Peças" :to="{ name: 'pecas' }" link></v-list-item>
        <v-list-item prepend-icon="mdi-account-group" title="Clientes" :to="{ name: 'home' }" link></v-list-item> <!-- Exemplo de item que leva para a home, onde clientes são exibidos -->
        <v-list-item prepend-icon="mdi-cog" title="Configurações" link></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- v-main: Área de Conteúdo Principal da Aplicação -->
    <!-- Esta área irá conter o conteúdo das suas views (páginas). -->
    <!-- O v-container que estava aqui foi movido para dentro das views (ex: HomeView.vue) para maior flexibilidade de layout. -->
    <v-main>
      <!-- RouterView: Componente do Vue Router que renderiza a view correspondente à rota atual. -->
      <RouterView />
    </v-main>

    <!-- v-footer: Rodapé da Aplicação (opcional) -->
    <!-- 'app' posiciona-o corretamente na aplicação. -->
    <!-- 'color="primary"' define a cor de fundo do rodapé. -->
    <!-- 'justify-center' alinha o conteúdo do rodapé ao centro. -->
    <v-footer app color="primary" class="justify-center">
      <!-- Exibição do ano atual e nome da assistência técnica -->
      <span class="white--text text-caption">&copy; {{ new Date().getFullYear() }} Assistência Técnica</span>
    </v-footer>
  </v-app>
</template>

<style>
/* Estilos globais para garantir que o scrollbar funcione corretamente */
html {
  overflow-y: auto; /* Permite scroll vertical se o conteúdo da página for maior que a altura da janela */
}
</style>
