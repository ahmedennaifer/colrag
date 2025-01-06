<!-- src/pages/TestPage.vue -->
<template>
    <q-page class="q-pa-md">
      <HelloComponent />
    </q-page>
  </template>
  
  <script>
  import HelloComponent from "components/HelloComponent.vue";
  
  export default {
    name: "TestPage",
    components: {
      HelloComponent,
    },
  };
  </script>
  