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
        :disabled="isSending"
        @input="adjustTextareaHeight"
      ></textarea>
      <button 
        @click="sendMessage" 
        :disabled="isSending" 
        :class="{ 'disabled': isSending }"
      >
        <i class="send-icon"></i>
      </button>
    </div>

    <!-- Warning Note Section -->
    <p class="info-text">*LLMs can make mistakes. Check important info.</p>
  </div>
</template>

---

### Script

```javascript
<script>
import axios from 'axios';

export default {
  name: 'ChatInterface',
  data() {
    return {
      userMessage: '',
      messages: [],
      isSending: false, // New state to manage send button state
      maxLines: 8, // Limit for textarea growth
    };
  },
  methods: {
    async sendMessage() {
      if (this.userMessage.trim() === '' || this.isSending) return;

      const message = this.userMessage; 
      this.messages.push({ text: message, isUser: true });
      this.userMessage = ''; // Clear input immediately
      this.isSending = true; // Disable input and button

      try {
        const response = await axios.post('http://127.0.0.1:8000/chat/', { message });
        const botReply = response.data;
        this.messages.push({ text: botReply, isUser: false });
      } catch (error) {
        console.error('Error communicating with the backend:', error);
        this.messages.push({ text: 'Error: Could not get a response from the model', isUser: false });
      } finally {
        this.isSending = false; // Re-enable input and button
      }
    },
    adjustTextareaHeight(event) {
      const textarea = event.target;
      textarea.style.height = 'auto'; // Reset height
      textarea.style.height = `${Math.min(textarea.scrollHeight, this.maxLines * 24)}px`; // Adjust height
    }
  }
};
</script>
<style>
/* GLOBAL CSS RESET: Ensure no browser defaults interfere */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Ensure html and body take the full height and background is applied */
html, body {
  height: 100vh;
  width: 100vw;
  background-color: #141414; /* Outside area background */
  overflow: hidden; /* Prevent any scrolling */
}

/* Chat container styling */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 95vh;
  width: 70vw;
  margin: auto;
  margin-top: 20px;
  background-color: #282828; /* Chat window background */
  border-radius: 15px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

/* Chat window area */
.chat-window {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  color: white;
  scrollbar-width: thin;
  scrollbar-color: #444 #282828;
}

/* Messages styling */
.message {
  margin: 8px 0;
}

.user {
  text-align: right;
  background-color: #3c3c3c;
  border-radius: 15px;
  padding: 10px;
  color: white;
}

.bot {
  text-align: left;
  background-color: #262621;
  border-radius: 15px;
  padding: 10px;
  color: white;
}

/* Chat input styling */
.chat-input {
  display: flex;
  align-items: flex-end;
  padding: 10px;
  gap: 10px;
  background-color: #1e1e1e;
  border-radius: 0 0 15px 15px;
}

.chat-input textarea {
  flex: 1;
  padding: 8px;
  border: 1px solid #333;
  border-radius: 15px;
  resize: none;
  overflow-y: hidden;
  font-size: 14px;
  background-color: #282828;
  color: white;
  outline: none;
}

.chat-input button {
  background-color: #007bff;
  border: none;
  padding: 10px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s;
}

.chat-input button.disabled {
  background-color: #999;
  cursor: not-allowed;
}

.chat-input button:hover:not(.disabled) {
  background-color: #0056b3;
}

/* Send icon */
.send-icon {
  width: 20px;
  height: 20px;
  background-image: url('https://img.icons8.com/ios-filled/50/ffffff/sent.png');
  background-size: contain;
  background-repeat: no-repeat;
}

/* Info text */
.info-text {
  text-align: center;
  font-size: 12px;
  color: #bbb;
  margin: 5px 0;
}
</style>
