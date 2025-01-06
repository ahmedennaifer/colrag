<template>
    <q-page class="q-pa-md">
      <DashboardComponent />
    </q-page>
  </template>
  
  <script>
  import DashboardComponent from 'components/DashboardComponent.vue';
  
  export default {
    name: "DashboardPage",
    components: {
      DashboardComponent,
    },
  };
  </script>
  