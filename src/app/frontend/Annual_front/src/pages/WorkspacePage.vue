<template>
    <q-page class="q-pa-md">
      <WorkspaceComponent />
    </q-page>
  </template>
  
  <script>
  import WorkspaceComponent from 'components/WorkspaceComponent.vue';
  
  export default {
    name: "WorkspacePage",
    components: {
      WorkspaceComponent,
    },
  };
  </script>
  