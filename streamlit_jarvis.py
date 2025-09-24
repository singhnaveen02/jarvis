
import streamlit as st
import requests
import json
import datetime
import wikipedia
import pyjokes
from io import BytesIO
import base64
import time

# Configure page for PWA
st.set_page_config(
    page_title="Mini Jarvis - AI Voice Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for PWA styling and mobile optimization
st.markdown("""
<style>
/* PWA Styling */
.main-header {
    text-align: center;
    color: #1f77b4;
    padding: 20px 0;
}

.chat-container {
    max-height: 400px;
    overflow-y: auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    margin: 20px 0;
    background-color: #f9f9f9;
}

.voice-controls {
    text-align: center;
    padding: 20px;
}

.assistant-response {
    background-color: #e3f2fd;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #1f77b4;
}

.user-input {
    background-color: #f1f8e9;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #4caf50;
}

/* Mobile optimization */
@media (max-width: 768px) {
    .main-container {
        padding: 10px;
    }

    .stButton > button {
        width: 100%;
        margin: 5px 0;
    }
}

/* Voice button styling */
.voice-btn {
    background: linear-gradient(45deg, #1f77b4, #42a5f5);
    color: white;
    border: none;
    border-radius: 50px;
    padding: 15px 30px;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.voice-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(31, 119, 180, 0.3);
}

/* Loading animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #1f77b4;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'reminders' not in st.session_state:
    st.session_state.reminders = []

class WebJarvis:
    def __init__(self):
        self.weather_api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with actual key
        self.weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def get_weather(self, city_name):
        """Get weather information using OpenWeatherMap API"""
        try:
            complete_url = f"{self.weather_base_url}appid={self.weather_api_key}&q={city_name}&units=metric"
            response = requests.get(complete_url)
            weather_data = response.json()

            if weather_data["cod"] != "404":
                main_data = weather_data["main"]
                weather_desc = weather_data["weather"][0]["description"]
                temperature = main_data["temp"]
                humidity = main_data["humidity"]

                return f"🌤️ The temperature in {city_name} is {temperature}°C with {weather_desc}. Humidity is {humidity}%."
            else:
                return f"❌ Sorry, I couldn't find weather information for {city_name}."

        except Exception as e:
            return "❌ Weather service unavailable. Please try again later."

    def wikipedia_search(self, query):
        """Search Wikipedia for information"""
        try:
            wikipedia.set_lang("en")
            result = wikipedia.summary(query, sentences=2)
            return f"📚 {result}"
        except wikipedia.exceptions.DisambiguationError as e:
            result = wikipedia.summary(e.options[0], sentences=2)
            return f"📚 {result}"
        except wikipedia.exceptions.PageError:
            return f"❌ Sorry, I couldn't find information about '{query}' on Wikipedia."
        except Exception as e:
            return "❌ Wikipedia search unavailable. Please try again later."

    def add_reminder(self, reminder_text):
        """Add a new reminder"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reminder = {
            "text": reminder_text,
            "created": current_time
        }
        st.session_state.reminders.append(reminder)
        return f"✅ Reminder added: {reminder_text}"

    def get_reminders(self):
        """Get all reminders"""
        if not st.session_state.reminders:
            return "📝 You have no reminders."

        reminder_list = "📝 Your reminders:\n"
        for i, reminder in enumerate(st.session_state.reminders, 1):
            reminder_list += f"{i}. {reminder['text']} (Added: {reminder['created']})\n"

        return reminder_list

    def get_time(self):
        """Get current time"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"🕐 The current time is {current_time}"

    def get_date(self):
        """Get current date"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"📅 Today is {current_date}"

    def tell_joke(self):
        """Tell a random joke"""
        try:
            joke = pyjokes.get_joke()
            return f"😄 {joke}"
        except:
            return "😄 Why don't scientists trust atoms? Because they make up everything!"

    def process_command(self, command):
        """Process user command and return response"""
        command = command.lower().strip()

        # Greeting commands
        if any(word in command for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
            hour = datetime.datetime.now().hour
            if 5 <= hour < 12:
                greeting = "Good morning!"
            elif 12 <= hour < 17:
                greeting = "Good afternoon!"
            else:
                greeting = "Good evening!"

            return f"👋 {greeting} I'm Mini Jarvis, your AI assistant. How can I help you today?"

        # Time and date commands
        elif 'time' in command:
            return self.get_time()

        elif 'date' in command or 'today' in command:
            return self.get_date()

        # Weather commands
        elif 'weather' in command:
            if 'in' in command:
                city_parts = command.split('in')
                if len(city_parts) > 1:
                    city = city_parts[1].strip()
                    return self.get_weather(city)
                else:
                    return "🌤️ Please specify a city name. For example: 'What's the weather in London?'"
            else:
                return "🌤️ Please specify a city name. For example: 'What's the weather in London?'"

        # Wikipedia search
        elif any(word in command for word in ['search', 'wikipedia', 'tell me about', 'what is', 'who is']):
            search_terms = ['search', 'wikipedia', 'tell me about', 'what is', 'who is']
            query = command
            for term in search_terms:
                if term in query:
                    query = query.replace(term, '').strip()
                    break

            if query:
                return self.wikipedia_search(query)
            else:
                return "🔍 What would you like me to search for?"

        # Reminder commands
        elif 'remind me' in command or 'add reminder' in command:
            if 'remind me' in command:
                reminder_text = command.replace('remind me', '').strip()
            else:
                reminder_text = command.replace('add reminder', '').strip()

            if reminder_text:
                return self.add_reminder(reminder_text)
            else:
                return "📝 What would you like me to remind you about?"

        elif 'my reminders' in command or 'show reminders' in command:
            return self.get_reminders()

        # Joke command
        elif 'joke' in command or 'funny' in command:
            return self.tell_joke()

        # Help command
        elif 'help' in command:
            return """🤖 I can help you with:

📅 **Time & Date**: "What time is it?", "What's the date?"
🌤️ **Weather**: "What's the weather in [city]?"
🔍 **Search**: "Tell me about [topic]", "What is [something]?"
📝 **Reminders**: "Remind me to [task]", "Show my reminders"
😄 **Entertainment**: "Tell me a joke"
👋 **Greeting**: Say hello anytime!

Just type or speak your request!"""

        # Default response
        else:
            return "🤔 I'm not sure how to help with that. Try asking about weather, time, Wikipedia searches, reminders, or jokes. Say 'help' for more options!"

# Initialize Jarvis
jarvis = WebJarvis()

# Main UI
st.markdown('<h1 class="main-header">🤖 Mini Jarvis - AI Voice Assistant</h1>', unsafe_allow_html=True)

# Voice input simulation (Web Speech API would be implemented with JavaScript)
st.markdown("""
<div class="voice-controls">
    <p><strong>💬 Voice commands available! (Simulated in this demo)</strong></p>
    <p>In a full PWA deployment, this would use Web Speech API for real voice input/output.</p>
</div>
""", unsafe_allow_html=True)

# Text input as fallback
user_input = st.text_input("💬 Type your message or command:", placeholder="Try: 'Hello', 'What time is it?', 'Weather in London'")

# Submit button
if st.button("🚀 Send Message") or user_input:
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "message": user_input})

        # Process command
        response = jarvis.process_command(user_input)

        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "message": response})

# Display chat history
if st.session_state.chat_history:
    st.markdown("## 💭 Conversation")

    for chat in st.session_state.chat_history[-10:]:  # Show last 10 messages
        if chat["role"] == "user":
            st.markdown(f'<div class="user-input"><strong>You:</strong> {chat["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-response"><strong>Jarvis:</strong> {chat["message"]}</div>', unsafe_allow_html=True)

# Sidebar with features
st.sidebar.title("🛠️ Features")
st.sidebar.info("""
**Available Commands:**
- 🕐 Time & Date queries
- 🌤️ Weather information
- 📚 Wikipedia search
- 📝 Reminder management
- 😄 Jokes & entertainment
- 💬 Natural conversation

**PWA Features:**
- 📱 Mobile responsive
- 🔄 Offline capable (partial)
- 🎙️ Voice integration ready
- 🌐 Cross-platform compatible
""")

# Quick action buttons
st.sidebar.markdown("### ⚡ Quick Actions")

if st.sidebar.button("🕐 Current Time"):
    response = jarvis.get_time()
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    st.experimental_rerun()

if st.sidebar.button("📅 Today's Date"):
    response = jarvis.get_date()
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    st.experimental_rerun()

if st.sidebar.button("😄 Tell a Joke"):
    response = jarvis.tell_joke()
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    st.experimental_rerun()

if st.sidebar.button("📝 Show Reminders"):
    response = jarvis.get_reminders()
    st.session_state.chat_history.append({"role": "assistant", "message": response})
    st.experimental_rerun()

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.experimental_rerun()

# PWA manifest and service worker info
st.markdown("""
---
### 📱 PWA Installation Instructions:

1. **Deploy to Streamlit Cloud**: Push this code to GitHub and deploy via [share.streamlit.io](https://share.streamlit.io)
2. **Add PWA Manifest**: Create `manifest.json` for app installation
3. **Implement Service Worker**: Add offline functionality with `sw.js`
4. **Enable Voice Features**: Integrate Web Speech API with custom JavaScript

**Alternative Deployment Options:**
- 🚀 **Vercel**: Deploy with serverless functions
- 🌐 **Netlify**: Static hosting with edge functions  
- ⚡ **GitHub Pages**: Free static hosting
""")
