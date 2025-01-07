<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="dashboard"
          aria-label="dashboard"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          CollRag
        </q-toolbar-title>

      </q-toolbar>
    </q-header>

    <!-- <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Essential Links
        </q-item-label>
        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer> -->

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useRouter } from 'vue-router'; 
import UserComponent from 'src/components/UserComponent.vue';

defineOptions({
  name: 'MainLayout'
})


const router = useRouter();

const toggleLeftDrawer = () => {
  router.push('/');
}

// return {
//   toggleLeftDrawer
// }
</script>

<style scoped>
.q-header {
background-color: #082038;
}

</style>

<style>

.q-page {
background-color: #6992b8;
}

</style>
