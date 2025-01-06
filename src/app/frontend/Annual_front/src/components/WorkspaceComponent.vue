<template>
  <q-page>
  <q-card class="workspace-card">
    <q-card-section class="workspace-header">
      <div class="text-h5">Gestion des Workspaces</div>
    </q-card-section>
    <q-card-section>
      <q-input 
        v-model="newWorkspace" 
        label="Nom du Workspace" 
        @keyup.enter="addWorkspace" 
        outlined
        class="workspace-input"
      />
      <q-btn 
        label="Ajouter Workspace" 
        color="primary" 
        @click="addWorkspace" 
        class="add-btn"
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
              class="remove-btn"
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
background-color: #92c5f8;
}

.workspace-card {
  background-color: #f7f9fb;
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  max-width: 600px;
  margin: 0px auto;
  overflow: hidden;
}

.workspace-header {
  background-color: #2196F3;
  color: white;
  padding: 20px;
  text-align: center;
  border-radius: 15px 15px 0 0;
}

.workspace-input {
  margin-bottom: 20px;
}

.add-btn {
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: scale(1.05);
  background-color: #1e88e5;
  box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
}

.workspace-list .workspace-item {
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.workspace-item:hover {
  transform: translateX(10px);
  background-color: #e3f2fd;
}

.remove-btn {
  transition: color 0.3s ease;
}

.remove-btn:hover {
  color: #d32f2f;
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
</style>
