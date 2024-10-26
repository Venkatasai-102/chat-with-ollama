<template>
  <div class="chat-container">
    <!-- Previous Chats Section -->
    <div class="chat-window">
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        class="message" 
        :class="{ 'user': msg.isUser, 'bot': !msg.isUser }"
      >
        <p>{{ msg.text }}</p>
      </div>
    </div>

    <!-- Text Input Section -->
    <div class="chat-input">
      <textarea 
        v-model="userMessage" 
        @keyup.enter="sendMessage" 
        placeholder="Type your message..." 
        rows="1"
        @input="adjustTextareaHeight"
      ></textarea>
      <button @click="sendMessage">
        <i class="send-icon"></i>
      </button>
    </div>

    <!-- Warning Note Section -->
    <p class="info-text">LLMs can make mistakes. Check important info.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatInterface',
  data() {
    return {
      userMessage: '',
      messages: [],
      maxLines: 10, // Limit for text area growth
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
    },
    adjustTextareaHeight(event) {
      const textarea = event.target;
      textarea.style.height = 'auto'; // Reset height to auto
      textarea.style.height = `${Math.min(textarea.scrollHeight, this.maxLines * 24)}px`; // Limit growth
    }
  }
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh; /* Full vertical height */
  width: 600px;
  margin: 0 auto;
  border: 1px solid #ccc;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 15px;
}

/* Chat Window: Holds previous chats and adjusts as input grows */
.chat-window {
  flex: 1; /* Takes most available space initially */
  padding: 15px;
  overflow-y: auto;
  border-bottom: 1px solid #ccc;
}

.message {
  margin: 8px 0;
}

.user {
  text-align: right;
  background-color: #e0ffe0;
  border-radius: 15px;
  padding: 10px;
}

.bot {
  text-align: left;
  background-color: #e0e0ff;
  border-radius: 15px;
  padding: 10px;
}

/* Chat Input: Flexible height with growing textarea */
.chat-input {
  display: flex;
  align-items: flex-end;
  padding: 10px;
  gap: 10px;
  background-color: #f8f8f8;
  border-bottom: 1px solid #ccc;
}

.chat-input textarea {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 15px;
  resize: none; /* Disable manual resizing */
  overflow-y: hidden; /* Avoid scrollbar */
  font-size: 14px;
}

.chat-input button {
  background-color: #007bff;
  border: none;
  padding: 10px;
  border-radius: 50%; /* Circle button */
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #0056b3;
}

/* Send Icon Styles */
.send-icon {
  width: 20px;
  height: 20px;
  background-image: url('https://img.icons8.com/ios-filled/50/ffffff/sent.png');
  background-size: contain;
  background-repeat: no-repeat;
}

/* Warning Text: Always at the bottom */
.info-text {
  text-align: center;
  font-size: 12px;
  color: #666;
  margin: 5px 0;
}
</style>
