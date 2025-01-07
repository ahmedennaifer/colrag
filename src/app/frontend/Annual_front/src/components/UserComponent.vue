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
        <q-input v-model="userData.firstName" label="Prénom" class="q-mb-md neon-input" />
        <q-input v-model="userData.lastName" label="Nom" class="q-mb-md neon-input" />
        <q-input v-model="userData.email" label="Email" type="email" readonly class="q-mb-md neon-input" />
      </q-card-section>
      
      <q-card-section class="q-pa-none">
        <div class="q-mb-md">
          <span class="text-h6 text-primary">Workspaces associés</span>
          <q-list bordered class="q-mt-xs">
            <q-item v-for="workspace in userData.workspaces" :key="workspace.id" class="neon-item">
              <q-item-section>{{ workspace.name }}</q-item-section>
            </q-item>
          </q-list>
        </div>
        
        <div>
          <span class="text-h6 text-primary">Documents associés</span>
          <q-list bordered class="q-mt-xs">
            <q-item v-for="document in userData.documents" :key="document.id" class="neon-item">
              <q-item-section>{{ document.name }}</q-item-section>
            </q-item>
          </q-list>
        </div>
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Mettre à jour"  @click="updateProfile" class="q-mb-md neon-btn" />
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
  background: linear-gradient(135deg, #121212, #1e1e2f);
  color: #e0e0e0;
}

.profile-card {
  max-width: 700px;
  margin: 0px auto;
  padding-left: 50px;
  padding-right: 50px;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background-color: #33334d;
}

.profile-img {
  border-radius: 50%;
  width: 100px;
  height: 100px;
  object-fit: cover;
  margin: 0 auto;
  border: 3px solid #d47f00;
}

.text-h6{
  color: #d47f00 !important;
}

.text-h5{
  font-weight: 600;
  color: #fff !important;
  margin-bottom: 20px;
  text-shadow: 0 0 15px #d47f00, 0 0 20px #00bcd4;

}

.neon-input {
  border-color: #d47f00 !important;
  color: white !important;
  background-color: #33334d;
  box-shadow: 0 0 10px #d47f00;
}

.neon-item {
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.neon-item:hover {
  transform: translateX(10px);
  background-color: #e3f2fd;
}

.neon-btn {
  margin-top: 10px;
  background-color: #d47f00;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 15px #00bcd4, 0 0 15px #00bcd4;
  transition: all 0.3s ease;
}

.neon-btn:hover {
  transform: scale(1.05);
  background-color: #d47f00;
  box-shadow: 0 4px 15px rgb(0,188,212);
}

.q-list {
  padding: 0;
  border-radius: 8px;
}

.q-item-section {
  font-weight: bold;
  color: white;
}

.q-item {
  padding: 8px 16px;
}

</style>
