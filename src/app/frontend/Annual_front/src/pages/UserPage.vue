<template>
  <q-page class="q-pa-md">
    <UserComponent :user="user" @update="updateUser" />
  </q-page>
</template>

<script>
import UserComponent from 'components/UserComponent.vue';

export default {
  name: "UserPage",
  components: {
    UserComponent,
  },
  data() {
    return {
      user: {
        name: "Nom utilisateur",
        email: "email@exemple.com",
      },
    };
  },  
  methods: {
    updateUser(updatedUser) {
      this.user = updatedUser;
    },
  },
};
</script>
