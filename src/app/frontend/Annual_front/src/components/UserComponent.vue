<template>
  <q-page>
  <q-card class="profile-card">
    <q-card-section class="text-center">
      <div class="text-h5 q-mb-md text-primary">Profil Utilisateur</div>
    </q-card-section>

    <q-card-section class="q-pa-none">
      <div class="q-mb-md">
        <q-img :src="userData.profilePicture" alt="Photo de profil" class="profile-img" />
      </div>
      <q-input v-model="userData.firstName" label="Prénom" class="q-mb-md" />
      <q-input v-model="userData.lastName" label="Nom" class="q-mb-md" />
      <q-input v-model="userData.email" label="Email" type="email" readonly class="q-mb-md" />
    </q-card-section>
    
    <q-card-section class="q-pa-none">
      <div class="q-mb-md">
        <span class="text-h6 text-primary">Workspaces associés</span>
        <q-list bordered class="q-mt-xs">
          <q-item v-for="workspace in userData.workspaces" :key="workspace.id">
            <q-item-section>{{ workspace.name }}</q-item-section>
          </q-item>
        </q-list>
      </div>
      
      <div>
        <span class="text-h6 text-primary">Documents associés</span>
        <q-list bordered class="q-mt-xs">
          <q-item v-for="document in userData.documents" :key="document.id">
            <q-item-section>{{ document.name }}</q-item-section>
          </q-item>
        </q-list>
      </div>
    </q-card-section>

    <q-card-actions align="right">
      <q-btn label="Mettre à jour" color="primary" @click="updateProfile" class="q-mb-md" />
    </q-card-actions>
  </q-card>
</q-page>
</template>

<script>
import { ref } from "vue";

export default {
  name: "UserProfile",
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit }) {
    const userData = ref({ ...props.user });

    const updateProfile = () => {
      emit("update", userData.value);
    };

    return {
      userData,
      updateProfile,
    };
  },
};
</script>

<style scoped>

.q-page {
background-color: #92c5f8;
}

.profile-card {
  max-width: 700px;
  margin: 0px auto;
  padding-left: 50px;
  padding-right: 50px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.profile-img {
  border-radius: 50%;
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin: 0 auto;
  border: 3px solid #007bff;
}

/* .q-card-section {
  padding: 16px;
} */

.text-primary {
  color: #007bff;
}

.q-btn {
  width: 150px;
}

.q-list {
  border-radius: 8px;
}

.q-item {
  padding: 8px 16px;
}

.q-item-section {
  font-weight: bold;
}
</style>
