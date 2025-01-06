<template>
  <q-page>
    <q-card class="profile-card">
      <q-card-section class="text-center">
        <div class="text-h5 q-mb-md text-primary">Créer un compte</div>
      </q-card-section>

      <q-card-section class="q-pa-none">
        <!--  -->
        <q-input v-model="signupData.firstName" label="Prénom" class="q-mb-md" />
        <q-input v-model="signupData.lastName" label="Nom" class="q-mb-md" />
        <q-input v-model="signupData.email" label="Email" type="email" class="q-mb-md" />
        <q-input 
          v-model="signupData.password" 
          label="Mot de passe" 
          type="password" 
          class="q-mb-md" 
        />
        <q-input 
          v-model="signupData.confirmPassword" 
          label="Confirmer le mot de passe" 
          type="password" 
          class="q-mb-md" 
        />
      </q-card-section>

      <q-card-actions align="right">
        <q-btn label="Créer un compte" color="primary" @click="register" class="q-mb-md" />
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

    // const handleFileUpload = (files) => {
    //   // Lire le fichier sélectionné
    //   const file = files[0];
    //   if (file) {
    //     const reader = new FileReader();
    //     reader.onload = (e) => {
    //       signupData.value.profilePicture = e.target.result; // Convertir en base64
    //     };
    //     reader.readAsDataURL(file);
    //   }
    // };

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
      // handleFileUpload,
      register,
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

.text-primary {
  color: #007bff;
}

.q-btn {
  width: 200px;
}
</style>
