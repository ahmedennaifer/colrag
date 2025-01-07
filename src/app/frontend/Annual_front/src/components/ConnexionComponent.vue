<template>
  <q-layout view="lHh LpR lFf">
    <q-page-container>
      <q-page class="flex flex-center">
        <q-card flat bordered class="login-card">
          <q-card-section class="connexion-header">
            <div class="text-h6 text-center animated fadeIn">Connexion</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit.prevent="handleLogin" ref="formRef">
              <q-input
                v-model="email"
                label="Adresse e-mail"
                type="email"
                outlined
                clearable
                dense
                :error="!!emailError"
                :error-message="emailError"
                class="input-field neon-input"
              />

              <q-input
                v-model="password"
                label="Mot de passe"
                type="password"
                outlined
                clearable
                dense
                class="q-mt-md input-field neon-input"
              />

              <q-btn
                type="submit"
                label="Se connecter"
                class="login-btn neon-btn full-width"
              />
            </q-form>
          </q-card-section>

          <q-card-actions align="center">
            <q-btn
              flat
              label="Créer un compte"
              color="secondary"
              @click="redirectToSignup"
              class="signup-btn neon-text"
            />
          </q-card-actions>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { useRouter } from 'vue-router'; 
import { ref } from 'vue';

export default {
  name: "ConnexionComponent",
  setup() {
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const emailError = ref('');
    const formRef = ref(null);

    const RegexEmail = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    const emailValidation = () => {
      if (RegexEmail.test(email.value)) {
        emailError.value = '';
        return true;
      } else {
        emailError.value = 'Adresse e-mail invalide';
        return false;
      }
    };

    const handleLogin = () => {
      const isEmailValid = emailValidation();

      if (!isEmailValid) {
        console.log('Erreur : Adresse e-mail invalide');
        return;
      }

      if (formRef.value.validate()) {
        console.log('Connexion réussie avec :', email.value, password.value); // Back en attente
      }
    };

    const redirectToSignup = () => {
      router.push('/signup');
    };

    return {
      email,
      password,
      emailError,
      formRef,
      handleLogin,
      redirectToSignup,
    };
  },
};
</script>

<style scoped>
/* Palette de fond */
.q-page {
  background: linear-gradient(135deg, #121212, #1e1e2f);
  color: #fff;
}

/* Carte de connexion */
.login-card {
  background: linear-gradient(145deg, #33334d, #4f4f72);
  border-radius: 30px;
  max-width: 400px;
  padding: 30px;
  width: 100%;
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.7), 0 0 20px rgba(221, 115, 15, 0.5);
  border: 1px solid rgba(221, 115, 15, 0.5);

}

/* En-tête de la connexion */
.connexion-header {
  background-color: #272741;
  color: white;
  padding: 20px;
  text-align: center;
  border-radius: 20px 20px 0 0;
  box-shadow: 0 4px 15px rgba(25, 118, 210, 0.5);
}

/* Texte du titre */
.text-h6 {
  font-weight: 600;
  color: #fff;
  margin-bottom: 20px;
  text-shadow: 0 0 15px #00bcd4, 0 0 20px #d47f00;
}

/* Style des inputs */
.input-field {
  transition: all 0.3s ease;
  color: #fff;
  border-color: #d47f00 ;
}
/* 
.q-field {
color: #fff !important; 
} */

.neon-input:focus-within {
  border-color: #d47f00 ;
}

.text-secondary {
    color: #d47f00 !important;
}

/* Bouton de connexion */
.login-btn {
  transition: all 0.3s ease;
  background-color: #d47f00;
  margin-top: 20px;
  color: white;
  border-radius: 10px;
  /* box-shadow: 0 0 10px #00bcd4, 0 0 10px #00bcd4; */
}

.login-btn:hover {
  transform: scale(1.05);
  background-color: #00bcd4;
  box-shadow: 0 4px 15px rgb(0,188,212);
}

/* Bouton de création de compte */
.signup-btn {
  color: #d47f00;
  font-weight: bold;
  transition: color 0.3s ease;
}

.signup-btn:hover {
  color: #d47f00;
  text-shadow: 0 0 10px #00bcd4, 0 0 20px #00bcd4;
}

/* Effet d'animation */
.animated {
  animation-duration: 0.5s;
  animation-timing-function: ease-out;
}

.fadeIn {
  animation-name: fadeIn;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
