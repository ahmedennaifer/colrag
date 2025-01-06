<template>
    <q-page class="flex flex-center">
      <div class="chat-container">
        <div class="messages">
          <div v-for="(message, index) in messages" :key="index" :class="{'sent': message.sent, 'received': !message.sent}">
            <p>{{ message.text }}</p>
          </div>
        </div>
        <q-input
          v-model="userMessage"
          @keyup.enter="sendMessage"
          outlined
          dense
          label="Tapez votre message"
          autofocus
        />
        <q-btn @click="sendMessage" label="Envoyer" color="primary" />
      </div>
    </q-page>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { QInput, QBtn } from 'quasar';
  
  export default {
    components: {
      QInput,
      QBtn
    },
    setup() {
      const userMessage = ref('');
      const messages = ref([]);
  
      const sendMessage = () => {
        if (userMessage.value.trim()) {
          messages.value.push({ text: userMessage.value, sent: true });
          userMessage.value = ''; 
        }
      };
  
      return {
        userMessage,
        messages,
        sendMessage
      };
    }
  };
  </script>
  
  <style scoped>
  .q-page {
  background-color: #92c5f8;
  }

  .chat-container {
    background-color: white;
    width: 100%;
    max-width: 500px;
    height: 400px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 10px;
  }
  
  .messages {
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 10px;
  }
  
  .messages .sent {
    text-align: right;
    background-color: #e0f7fa;
    padding: 5px;
    border-radius: 5px;
  }
  
  .messages .received {
    text-align: left;
    background-color: #f1f1f1;
    padding: 5px;
    border-radius: 5px;
  }
  
  q-input {
    margin-top: 10px;
  }
  </style>
  