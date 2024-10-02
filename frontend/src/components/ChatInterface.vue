<template>
  <div class="chat-container">
    <div class="chat-window">
      <div v-for="(msg, index) in messages" :key="index" class="message" :class="{'user': msg.isUser, 'bot': !msg.isUser}">
        <p>{{ msg.text }}</p>
      </div>
    </div>

    <div class="chat-input">
      <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Type your message..." />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
name: 'ChatInterface', // Update the component name
data() {
  return {
    userMessage: '',
    messages: [],
  };
},
methods: {
  async sendMessage() {
    if (this.userMessage.trim() === '') return;

    this.messages.push({ text: this.userMessage, isUser: true });

    const requestData = { message: this.userMessage };

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat/', requestData);
      const botReply = response.data;

      this.messages.push({ text: botReply, isUser: false });
    } catch (error) {
      console.error('Error communicating with the backend:', error);
      this.messages.push({ text: 'Error: Could not get a response from the model', isUser: false });
    }

    this.userMessage = '';
  }
}
};
</script>


<style scoped>
.chat-container {
  width: 400px;
  margin: 0 auto;
}

.chat-window {
  height: 400px;
  border: 1px solid #ccc;
  padding: 10px;
  overflow-y: auto;
}

.message {
  margin: 5px 0;
}

.user {
  text-align: right;
  background-color: #e0ffe0;
}

.bot {
  text-align: left;
  background-color: #e0e0ff;
}

.chat-input {
  display: flex;
  margin-top: 10px;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
}

.chat-input button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
}
</style>
