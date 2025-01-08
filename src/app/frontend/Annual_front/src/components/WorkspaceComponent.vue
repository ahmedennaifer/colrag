<template>
  <q-page>
    <q-card class="workspace-card">
      <q-card-section class="workspace-header animated fadeIn">
        <div class="text-h5">Gestion des Workspaces</div>
      </q-card-section>
      <q-card-section>
        <q-input 
          v-model="newWorkspace" 
          label="Nom du Workspace" 
          @keyup.enter="addWorkspace" 
          outlined
          class="workspace-input neon-input"
        />
        <q-btn 
          label="Ajouter Workspace" 
          @click="addWorkspace" 
          class="add-btn neon-btn"
        />
      </q-card-section>
      <q-card-section>
        <q-list bordered separator class="workspace-list">
          <q-item v-for="(workspace, index) in workspaces" :key="index" class="workspace-item">
            <q-item-section>{{ workspace.name }}</q-item-section>
            <q-item-section side>
              <q-btn 
                icon="delete" 
                color="negative" 
                flat 
                round 
                @click="removeWorkspace(index)" 
                class="remove-btn neon-btn"
              />
            </q-item-section>
          </q-item>
        </q-list>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref } from "vue";

export default {
  name: "WorkspaceComponent",
  setup() {
    const newWorkspace = ref("");
    const workspaces = ref([
      { name: "Workspace 1" },
      { name: "Workspace 2" },
    ]);

    const addWorkspace = () => {
      if (newWorkspace.value.trim() !== "") {
        workspaces.value.push({ name: newWorkspace.value });
        newWorkspace.value = "";
      }
    };

    const removeWorkspace = (index) => {
      workspaces.value.splice(index, 1);
    };

    return {
      newWorkspace,
      workspaces,
      addWorkspace,
      removeWorkspace,
    };
  },
};
</script>

<style scoped>
.q-page {
  background: linear-gradient(135deg, #121212, #1e1e2f);
  color: #e0e0e0;
}

.workspace-card {
  background: linear-gradient(145deg, #33334d, #4f4f72);
  border-radius: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.7), 0 0 20px rgba(221, 115, 15, 0.5);
  max-width: 600px;
  margin: 0px auto;
  padding: 30px;
  overflow: hidden;
}

.text-h5 {
  font-weight: 600;
  color: #fff;
  margin-bottom: 20px;
  text-shadow: 0 0 15px #d47f00, 0 0 20px #00bcd4;
}

/* En-tête */
.workspace-header {
  color: white;
  padding: 20px;
  text-align: center;
  border-radius: 15px 15px 0 0;
  text-shadow: 0 0 15px #d47f00, 0 0 20px #d47f00;
}

/* Champ de saisie et bouton d'ajout */
.workspace-input,
.neon-input:focus-within {
  border-color: #d47f00 !important;
  color: white !important;
  transition: all 0.3s ease;
}

/* Bouton d'ajout */
.add-btn {
  margin-top: 20px;
  background-color: #d47f00;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px #d47f00, 0 0 10px #d47f00;
  transition: all 0.3s ease;
}

.q-field .q-field__control{
  color: white!important;
}

.q-field__native{
  color: white !important;
}

.add-btn:hover {
  transform: scale(1.05);
  background-color: #d47f00;
  box-shadow: 0 4px 15px rgba(221, 115, 15, 0.5);
}

/* Liste des workspaces */
.workspace-list .workspace-item {
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.workspace-item:hover {
  transform: translateX(10px);
  /* background-color: #e3f2fd; */
}

.remove-btn {
  color: white;
  transition: color 0.3s ease;
}

.remove-btn:hover {
  color: #d32f2f;
  text-shadow: 0 0 10px #d47f00, 0 0 20px #d47f00;
}

.q-item-section {
  transition: padding 0.3s ease;
}

.q-item-section:hover {
  padding-left: 15px;
}

.workspace-item {
  margin-bottom: 10px;
}

.workspace-list {
  padding: 0;
}

/* Animation de fade-in */
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
