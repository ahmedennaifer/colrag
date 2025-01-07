<template>
  <q-page class="flex flex-center">
    <div class="chat-container animated fadeIn">
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
        class="neon-input"
      />
      <q-btn @click="sendMessage" label="Envoyer" class="neon-btn" />
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
  background: linear-gradient(135deg, #121212, #1e1e2f);
  color: #e0e0e0;
}

.chat-container {
  background: linear-gradient(145deg, #33334d, #4f4f72);
  width: 100%;
  max-width: 500px;
  height: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid #ccc;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7), 0 0 20px rgba(221, 115, 15, 0.5);
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px;
  color: white;
}

.messages .sent {
  text-align: right;
  background-color: #4caf50;
  padding: 10px;
  border-radius: 10px;
  color: white;
  box-shadow: 0 0 10px #4caf50;
}

.messages .received {
  text-align: left;
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 10px;
  color: white;
  box-shadow: 0 0 10px #f1f1f1;
}

.neon-input {
  border-color: #d47f00 !important;
  color: white !important;
  background-color: #33334d;
  box-shadow: 0 0 10px #d47f00;
}

.neon-btn {
  margin-top: 10px;
  background-color: #d47f00;
  color: white;
  border-radius: 10px;
  box-shadow: 0 0 15px #d47f00, 0 0 15px #d47f00;
  transition: all 0.3s ease;
}

.neon-btn:hover {
  transform: scale(1.05);
  background-color: #d47f00;
  box-shadow: 0 4px 15px rgba(221, 115, 15, 0.5);
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
