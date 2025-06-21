import { createRouter, createWebHistory } from 'vue-router'
// IMPORTANTE: O caminho para suas views aqui deve ser relativo à pasta 'router'
// Se suas views estão em src/views/, então o caminho de router/index.js é ../views/
import HomeView from '../views/HomeView.vue' // Corrigido o caminho
import OrdensServicoView from '../views/OrdensServicoView.vue' // Corrigido o caminho
import OrdemServicoDetalheView from '../views/OrdemServicoDetalheView.vue' // Corrigido o caminho
import OrdemServicoCreateView from '../views/OrdemServicoCreateView.vue' // Corrigido o caminho
import OrdemServicoEditView from '../views/OrdemServicoEditView.vue' // Corrigido o caminho
import PecaListView from '../views/PecaListView.vue' // Corrigido o caminho
import PecaCreateView from '../views/PecaCreateView.vue' // Corrigido o caminho

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
    {
      path: '/ordens-servico/abrir',
      name: 'os-abrir',
      component: OrdemServicoCreateView
    },
    {
      path: '/ordens-servico/:id/editar',
      name: 'os-editar',
      component: OrdemServicoEditView,
      props: true
    },
    {
      path: '/ordens-servico/:id',
      name: 'os-detalhe',
      component: OrdemServicoDetalheView,
      props: true
    },
    {
      path: '/pecas',
      name: 'pecas',
      component: PecaListView
    },
    {
      path: '/pecas/criar',
      name: 'peca-criar',
      component: PecaCreateView
    }
  ]
})

export default router