<template>
  <q-page>
  <q-card class="card">
    <div class="dash_center q-pa-md">
      <div class="text-h5 q-pa-md animated fadeIn">Tableau de Bord</div>
      <q-list>
        <q-item v-for="(item, index) in menu" :key="index" clickable v-ripple :to="item.route" class="animated fadeInUp">
          <q-item-section avatar>
            <q-icon :name="item.icon" class="icon-animate"/>
          </q-item-section>
          <q-item-section>{{ item.label }}</q-item-section>
        </q-item>
      </q-list>

      <!-- Animation Loader -->
      <div v-if="isLoading" class="loading-container">
        <q-spinner-dots color="primary" size="40px" />
      </div>
    </div>
  </q-card>
</q-page>
</template>

<script>
export default {
  name: "DashboardComponent",
  setup() {
    const menu = [
      { label: 'Profil', route: '/user', icon: 'account_circle' },
      { label: 'Workspaces', route: '/workspace', icon: 'workspaces' },
      { label: 'Connexion', route: '/connexion', icon: 'login' },
      { label: 'Documents', route: '/documents', icon: 'folder' },
      { label: 'RaggyChat', route: '/chatbot', icon: 'smart_toy' },
      // { label: 'Sign', route: '/signup', icon: 'smart_toy' },
    ];
    const isLoading = false; 

    return { menu, isLoading };
  }
};
</script>

<style scoped>

.dash_center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100px;
  text-align: center;
  margin-right: auto;
}
.q-page {
background-color: #92c5f8;
}

.card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 750px;
  max-width: 250px;
  margin: 0 auto;
  background-color: #abf1ec;
  border-radius: 50px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.text-h5 {
  font-weight: 600;
  color: #182027;
  margin-bottom: 20px;
}

.q-item {
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.q-item:hover {
  transform: scale(1.05);
  background-color: #e1f5fe;
}

.icon-animate {
  transition: transform 0.3s ease;
}

.q-item:hover .icon-animate {
  transform: rotate(20deg);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.animated {
  animation-duration: 0.5s;
  animation-timing-function: ease-out;
}

.fadeIn {
  animation-name: fadeIn;
}

.fadeInUp {
  animation-name: fadeInUp;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
