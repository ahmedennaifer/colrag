
import { createRouter, createWebHistory } from 'vue-router';
import { useQuasar } from 'quasar';

const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('components/DashboardComponent.vue') },
      { path: '/dashboard', component: () => import('components/DashboardComponent.vue') },
      { path: '/test', component: () => import('components/HelloComponent.vue') },
      { path: '/user', component: () => import('components/UserComponent.vue') },
      { path: '/connexion', component: () => import('components/ConnexionComponent.vue') },
      { path: '/signup', component: () => import('components/SignupComponent.vue') },
      { path: '/workspace', component: () => import('components/WorkspaceComponent.vue') },
      { path: '/documents', component: () => import('components/DocumentComponent.vue') },
      { path: '/chatbot', component: () => import('components/ChatComponent.vue') },


    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const $q = useQuasar();
  // Affiche le spinner global pendant le chargement
  $q.loading.show();
  next();
});

router.afterEach(() => {
  const $q = useQuasar();
  // Cache le spinner après la navigation
  $q.loading.hide();
});

export default routes
