<!-- src/pages/User.vue -->
<template>
    <q-page class="q-pa-md">
      <q-card>
        <q-card-section>
          <h2>Mon profil</h2>
        </q-card-section>
        <q-card-section>
          <q-input v-model="name" label="Nom" />
          <q-input v-model="email" label="Email" type="email" readonly />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn label="Mettre à jour" color="primary" @click="updateProfile" />
        </q-card-actions>
      </q-card>
    </q-page>
  </template>
  
  <script>
  export default {
    name: "UserPage",
    data() {
      return {
        name: "Nom utilisateur",
        email: "email@exemple.com",
      };
    },
    methods: {
      updateProfile() {
        // Logique de mise à jour du profil
      },
    },
  };
  </script>
  