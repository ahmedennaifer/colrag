const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: '/login', component: () => import('pages/Login.vue') },
      { path: '/signup', component: () => import('pages/Signup.vue') },
      { path: '/user', component: () => import('pages/User.vue') },
      { path: '/workspace', component: () => import('pages/Workspace.vue') },
       { path: '/docs', component: () => import('pages/Docs.vue') },
      { path: '/dashboard', component: () => import('pages/Dashboard.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
