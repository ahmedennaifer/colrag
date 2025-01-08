<template>
  <q-page>
    <q-card class="profile-card">
      <q-card-section class="text-center">
        <div class="text-h5 q-mb-md text-primary">Créer un compte</div>
      </q-card-section>

      <q-card-section class="q-pa-none">
        <q-input v-model="signupData.firstName" label="Prénom" class="q-mb-md neon-input" />
        <q-input v-model="signupData.lastName" label="Nom" class="q-mb-md neon-input" />
        <q-input v-model="signupData.email" label="Email" type="email" class="q-mb-md neon-input" />
        <q-input 
          v-model="signupData.password" 
          label="Mot de passe" 
          type="password" 
          class="q-mb-md neon-input"
        />
        <q-input 
          v-model="signupData.confirmPassword" 
          label="Confirmer le mot de passe" 
          type="password" 
          class="q-mb-md neon-input"
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Créer un compte"  @click="register" class="q-mb-md neon-btn" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script>
import { ref } from "vue";

export default {
  name: "SignUp",
  setup() {
    const signupData = ref({
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      confirmPassword: "",
      profilePicture: null, // URL de la photo téléchargée
    });

    const register = () => {
      if (signupData.value.password !== signupData.value.confirmPassword) {
        alert("Les mots de passe ne correspondent pas !");
        return;
      }
      // Envoyer les données au backend ou traiter localement
      console.log("Données d'inscription :", signupData.value);
      alert("Inscription réussie !");
    };

    return {
      signupData,
      register,
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

/* .text-primary {
  color: #d47f00;
} */

.neon-input {
  border-color: #d47f00 !important;
  color: white !important;
  background-color: #33334d;
  box-shadow: 0 0 10px #d47f00;
}

.text-h5{
  font-weight: 600;
  color: #fff !important;
  margin-bottom: 20px;
  text-shadow: 0 0 15px #d47f00, 0 0 20px #00bcd4;
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
</style>
