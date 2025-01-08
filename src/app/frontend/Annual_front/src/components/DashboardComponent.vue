<template>
  <q-page>
    <q-card class="card">
      <div class="dash_center q-pa-md">
        <div class="text-h5 q-pa-md animated fadeIn">Tableau de Bord</div>
        <q-list>
          <q-item 
            v-for="(item, index) in menu" 
            :key="index" 
            clickable 
            v-ripple 
            :to="item.route" 
            class="q-item neon-hover animated fadeInUp"
          >
            <q-item-section avatar>
              <q-icon :name="item.icon" class="icon-animate neon-icon" />
            </q-item-section>
            <q-item-section>{{ item.label }}</q-item-section>
          </q-item>
        </q-list>

        <!-- Animation Loader -->
        <div v-if="isLoading" class="loading-container">
          <q-spinner-dots color="accent" size="40px" />
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
    ];
    const isLoading = false;

    return { menu, isLoading };
  }
};
</script>

<style scoped>
/* Palette de fond */
.q-page {
  background: linear-gradient(135deg, #121212, #1e1e2f);
  color: #e0e0e0;
}

/* Style de la carte */
.card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: auto;
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(145deg, #1b1b29, #272741);
  border-radius: 30px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.7), 0 0 20px rgba(221, 115, 15, 0.5);
  border: 1px solid rgba(221, 115, 15, 0.5);
}

/* Titre */
.text-h5 {
  font-weight: 600;
  color: #fff !important;
  margin-bottom: 20px;
  text-shadow: 0 0 15px #d47f00, 0 0 20px #00bcd4;
}

/* Liste des éléments */
.q-item {
  padding: 10px;
  border-radius: 10px;
  margin: 10px 0;
  background: linear-gradient(145deg, #222230, #2b2b40);
  color: #e0e0e0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

/* Effet de survol */
.q-item:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px #d47f00, 0 0 20px #00bcd4;
  background: linear-gradient(145deg, #2b2b40, #343454);
}

/* Icônes néons */
.icon-animate {
  font-size: 24px;
  color: #d47f00;
  transition: transform 0.3s ease, color 0.3s ease;
}

.icon-animate.neon-icon:hover {
  transform: rotate(15deg) scale(1.2);
  color: #00bcd4;
}

/* Conteneur du loader */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

/* Animations */
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
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Survol néon */
.neon-hover:hover {
  background: linear-gradient(145deg, #2f2f4a, #3b3b5f);
  box-shadow: 0 0 20px #00bcd4, 0 0 20px #00bcd4;
}
</style>
