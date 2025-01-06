<template>
    <q-layout view="lHh LpR lFf">
      <!-- En-tête -->
      <q-header elevated class="bg-primary text-white">
        <q-toolbar>
          <q-toolbar-title>
            <span>Rag Connexion</span>
          </q-toolbar-title>
        </q-toolbar>
      </q-header>
  
      <!-- Page principale -->
      <q-page-container>
        <q-page class="flex flex-center">
          <q-card flat bordered class="q-pa-md q-mt-lg" style="max-width: 400px;">
            <q-card-section>
              <div class="text-h6 text-center">Connexion</div>
            </q-card-section>
  
            <q-card-section>
              <q-form @submit.prevent="handleLogin" ref="formRef">
                <!-- Champ e-mail -->
                <q-input
                  v-model="email"
                  label="Adresse e-mail"
                  type="email"
                  :rules="[rules.required, rules.email]"
                  outlined
                  clearable
                  dense
                />
  
                <!-- Champ mot de passe -->
                <q-input
                  v-model="password"
                  label="Mot de passe"
                  type="password"
                  :rules="[rules.required]"
                  outlined
                  clearable
                  dense
                  class="q-mt-md"
                />
  
                <!-- Bouton de connexion -->
                <q-btn
                  type="submit"
                  label="Se connecter"
                  color="primary"
                  class="q-mt-lg full-width"
                />
              </q-form>
            </q-card-section>
  
            <q-card-actions align="center">
              <q-btn
                flat
                label="Créer un compte"
                color="secondary"
                @click="redirectToSignup"
              />
            </q-card-actions>
          </q-card>
        </q-page>
      </q-page-container>
    </q-layout>
  </template>
  
  <script setup>
 
  </script>
  
  <style scoped>
  .q-card {
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  </style>
  