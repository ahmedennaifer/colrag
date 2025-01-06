<template>
  <q-layout view="lHh LpR lFf">
    <q-page-container>
      <q-page class="flex flex-center">
        <q-card flat bordered class="q-pa-md q-mt-lg login-card">
          <q-card-section class="connexion-header">
            <div class="text-h6 text-center">Connexion </div>
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
                class="input-field"
              />

              <q-input
                v-model="password"
                label="Mot de passe"
                type="password"
                outlined
                clearable
                dense
                class="q-mt-md input-field"
              />

              <q-btn
                type="submit"
                label="Se connecter"
                color="primary"
                class="login-btn full-width"
              />
            </q-form>
          </q-card-section>

          <q-card-actions align="center">
            <q-btn
              flat
              label="Créer un compte"
              color="secondary"
              @click="redirectToSignup"
              class="signup-btn"
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
      // console.log('Redirection vers la page de création de compte...');
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

.q-page {
background-color: #92c5f8;
}

.login-card {
  background-color: #fbf9f7;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
  max-width: 400px;
  width: 100%;
  padding: 30px;
  overflow: hidden;
}

.connexion-header {
  background-color: #2196F3;
  color: white;
  padding: 20px;
  text-align: center;
  border-radius: 15px 15px 0 0;
}

.text-h6 {
  font-weight: 600;
  color: #f7f9fb;
  margin-bottom: 20px;
}

.input-field {
  transition: all 0.3s ease;
}

.input-field:focus-within {
  border-color: #2196f3;
}

.login-btn {
  transition: all 0.3s ease;
}

.login-btn:hover {
  transform: scale(1.05);
  background-color: #1976d2;
  box-shadow: 0 4px 15px rgba(25, 118, 210, 0.5);
}

.signup-btn {
  transition: color 0.3s ease;
}

.signup-btn:hover {
  color: #1976d2;
}

.q-card-actions {
  margin-top: 20px;
}

.q-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.q-card-section {
  padding: 10px 0;
}
</style>
