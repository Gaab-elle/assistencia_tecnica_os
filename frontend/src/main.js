// assistencia_tecnica_os/frontend/src/main.js

// Importa estilos CSS globais (se você tiver um)
import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// >>> Vuetify: Início da configuração NECESSÁRIA <<<
import 'vuetify/styles' // 1. Importa os estilos CSS do Vuetify
import { createVuetify } from 'vuetify' // 2. Importa a função para criar a instância do Vuetify
import * as components from 'vuetify/components' // 3. Importa todos os componentes do Vuetify (VBtn, VApp, etc.)
import * as directives from 'vuetify/directives' // 4. Importa as diretivas do Vuetify (como v-tooltip)
import { aliases, mdi } from 'vuetify/iconsets/mdi' // 5. Importa a configuração para ícones Material Design Icons

// Cria a instância do Vuetify
const vuetify = createVuetify({
  components, // Registra os componentes
  directives, // Registra as diretivas
  icons: { // Configurações de ícones
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})


const app = createApp(App) // Cria a aplicação Vue

app.use(router) // Diz à aplicação Vue para usar o Vue Router
app.use(vuetify) // <<< MUITO IMPORTANTE: Diz à aplicação Vue para usar o Vuetify

app.mount('#app') // Monta a aplicação Vue no elemento com id="app" no seu index.html