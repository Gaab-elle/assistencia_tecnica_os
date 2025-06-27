// assistencia_tecnica_os/frontend/src/main.js

// Importa estilos CSS globais (se você tiver um)
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// >>> Vuetify: Início da configuração <<<
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi' // Para ícones Material Design

// Cria a instância do Vuetify
const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  // >>> Personalização de Cores: Tema MICLEO <<<
  theme: {
    defaultTheme: 'miceloDark', // Define seu novo tema como o padrão
    themes: {
      miceloDark: { // Definições para o tema 'miceloDark'
        dark: true, // Indica que este é um tema escuro
        colors: {
          // Cores base do tema MICLEO
          primary: '#1A202E', // Fundo principal escuro (similar ao da imagem)
          secondary: '#36405F', // Cor de destaque para cards, sidebar (azul mais escuro)
          accent: '#00BCD4', // Exemplo de ciano para acentos (pode ser ajustado)
          info: '#2196F3',   // Azul padrão para info
          success: '#4CAF50', // Verde para sucesso
          warning: '#FFC107', // Amarelo para aviso
          error: '#FF5252',   // Vermelho para erro

          // Cores de texto e superfícies
          background: '#12161F', // Fundo mais escuro ainda para o corpo da página
          surface: '#1A202E',    // Superfícies como cards e fundos de elementos
          'on-surface': '#FFFFFF', // Cor do texto em cima das superfícies (branco)
          'on-background': '#E0E0E0', // Cor do texto no fundo (cinza claro)
        },
      },
      // Você pode manter ou remover o tema 'light' se não for usá-lo
      light: {
        colors: {
          primary: '#1976D2',
          secondary: '#424242',
          accent: '#82B1FF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
        },
      },
    },
  },
})
// >>> Vuetify: Fim da configuração <<<


const app = createApp(App)

app.use(router)
app.use(vuetify)

app.mount('#app')