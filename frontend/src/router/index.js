import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import OrdensServicoView from '../views/OrdensServicoView.vue'
import OrdemServicoDetalheView from '../views/OrdemServicoDetalheView.vue'
import OrdemServicoCreateView from '../views/OrdemServicoCreateView.vue'
import OrdemServicoEditView from '../views/OrdemServicoEditView.vue'
import PecaListView from '../views/PecaListView.vue'
import PecaCreateView from '../views/PecaCreateView.vue' // Importa a nova View de Criação de Peças

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ordens-servico',
      name: 'ordens-servico',
      component: OrdensServicoView
    },
    { // Rota para criar nova OS
      path: '/ordens-servico/abrir',
      name: 'os-abrir',
      component: OrdemServicoCreateView
    },
    { // Rota para editar OS (com ID) - DEVE VIR ANTES da rota de detalhes da OS
      path: '/ordens-servico/:id/editar',
      name: 'os-editar',
      component: OrdemServicoEditView,
      props: true // Passa o parâmetro 'id' da rota como prop para a view
    },
    { // Rota para detalhes da OS (com ID)
      path: '/ordens-servico/:id',
      name: 'os-detalhe',
      component: OrdemServicoDetalheView,
      props: true
    },
    { // Rota para a Listagem de Peças
      path: '/pecas',
      name: 'pecas',
      component: PecaListView
    },
    { // Rota para criar nova Peça
      path: '/pecas/criar',
      name: 'peca-criar',
      component: PecaCreateView
    }
    // Você adicionará outras rotas aqui conforme criar novos módulos
  ]
})

export default router