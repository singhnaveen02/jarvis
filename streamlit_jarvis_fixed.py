import streamlit as st
import requests
import datetime
import wikipedia
import pyjokes

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Mini Jarvis - AI Voice Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM STYLING --------------------
st.markdown("""
<style>
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
@media (max-width: 768px) {
    .main-container { padding: 10px; }
    .stButton > button { width: 100%; margin: 5px 0; }
}
</style>
""", unsafe_allow_html=True)

# -------------------- SESSION STATE --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "reminders" not in st.session_state:
    st.session_state.reminders = []

# -------------------- JARVIS CLASS --------------------
class WebJarvis:
    def __init__(self):
        self.weather_api_key = "a51eaca1954a256f122d4f1c8d4290b2"
        self.weather_base_url = "https://api.openweathermap.org/data/2.5/weather?"
        st.info("💡 Lightweight version - Advanced NLP features disabled for faster deployment")

    # WEATHER
    def get_weather(self, city_name: str) -> str:
        try:
            city_name = city_name.strip().replace(" ", "+")
            url = f"{self.weather_base_url}appid={self.weather_api_key}&q={city_name}&units=metric"
            response = requests.get(url)
            data = response.json()

            if int(data.get("cod", 404)) != 404:
                main = data["main"]
                weather_desc = data["weather"][0]["description"]
                return f"🌤️ {city_name}: {main['temp']}°C, {weather_desc}. Humidity {main['humidity']}%."
            else:
                return f"❌ Couldn't find weather for {city_name}. (Reason: {data.get('message')})"
        except Exception as e:
            return f"❌ Error: {str(e)}"

    # WIKIPEDIA
    def wikipedia_search(self, query: str) -> str:
        try:
            wikipedia.set_lang("en")
            return f"📚 {wikipedia.summary(query, sentences=2)}"
        except wikipedia.exceptions.DisambiguationError as e:
            return f"📚 {wikipedia.summary(e.options[0], sentences=2)}"
        except wikipedia.exceptions.PageError:
            return f"❌ No results found for '{query}'."
        except Exception:
            return "❌ Wikipedia search unavailable."

    # REMINDERS
    def add_reminder(self, text: str) -> str:
        st.session_state.reminders.append({
            "text": text,
            "created": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return f"✅ Reminder added: {text}"

    def get_reminders(self) -> str:
        if not st.session_state.reminders:
            return "📝 You have no reminders."
        reminders = [f"{i+1}. {r['text']} (Added: {r['created']})"
                     for i, r in enumerate(st.session_state.reminders)]
        return "📝 Your reminders:\n" + "\n".join(reminders)

    # TIME & DATE
    def get_time(self) -> str:
        return f"🕐 Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"

    def get_date(self) -> str:
        return f"📅 Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}"

    # JOKES
    def tell_joke(self) -> str:
        try:
            return f"😄 {pyjokes.get_joke()}"
        except:
            return "😄 Why don't scientists trust atoms? Because they make up everything!"

    # COMMAND PROCESSOR
    def process_command(self, command: str) -> str:
        command = command.lower().strip()

        # Greetings
        if any(word in command for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]):
            hour = datetime.datetime.now().hour
            greeting = "Good morning!" if 5 <= hour < 12 else "Good afternoon!" if 12 <= hour < 17 else "Good evening!"
            return f"👋 {greeting} I'm Mini Jarvis. How can I help?"

        # Time & Date
        if "time" in command:
            return self.get_time()
        if "date" in command or "today" in command:
            return self.get_date()

        # Weather
        if "weather" in command:
            if "in" in command:
                city = command.split("in")[-1].strip()
                return self.get_weather(city)
            return "🌤️ Please specify a city. Example: 'Weather in London'"

        # Wikipedia
        if any(term in command for term in ["search", "wikipedia", "tell me about", "what is", "who is"]):
            query = command
            for term in ["search", "wikipedia", "tell me about", "what is", "who is"]:
                query = query.replace(term, "").strip()
            return self.wikipedia_search(query) if query else "🔍 What should I search for?"

        # Reminders
        if "remind me" in command or "add reminder" in command:
            text = command.replace("remind me", "").replace("add reminder", "").strip()
            return self.add_reminder(text) if text else "📝 What should I remind you about?"
        if "reminders" in command:
            return self.get_reminders()

        # Jokes
        if "joke" in command or "funny" in command:
            return self.tell_joke()

        # Help
        if "help" in command:
            return """🤖 I can help with:
📅 Time & Date → "What time is it?", "What's the date?"
🌤️ Weather → "Weather in [city]"
🔍 Wikipedia → "Tell me about [topic]"
📝 Reminders → "Remind me to [task]", "Show reminders"
😄 Jokes → "Tell me a joke"
👋 Greetings → Say hello!"""

        return "🤔 I'm not sure. Try 'help' for available commands."

# -------------------- INITIALIZE --------------------
jarvis = WebJarvis()

# -------------------- MAIN UI --------------------
st.markdown('<h1 class="main-header">🤖 Mini Jarvis - AI Voice Assistant</h1>', unsafe_allow_html=True)
st.success("✅ Deployment-Optimized Version - Faster Loading!")

# Voice simulation
st.markdown("""
<div class="voice-controls">
    <p><strong>💬 Ready for commands!</strong></p>
    <p>💡 Use st.audio_input (in sidebar) for voice recording</p>
</div>
""", unsafe_allow_html=True)

# User input
user_input = st.text_input("💬 Type your message or command:", placeholder="Try: 'Hello', 'Weather in London'")

if st.button("🚀 Send Message") or user_input:
    if user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        st.session_state.chat_history.append({"role": "assistant", "message": jarvis.process_command(user_input)})

# Chat history
if st.session_state.chat_history:
    st.markdown("## 💭 Conversation")
    for chat in st.session_state.chat_history[-10:]:
        css_class = "user-input" if chat["role"] == "user" else "assistant-response"
        prefix = "You" if chat["role"] == "user" else "Jarvis"
        st.markdown(f'<div class="{css_class}"><strong>{prefix}:</strong> {chat["message"]}</div>', unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("🛠️ Features")

# Voice
st.sidebar.markdown("### 🎙️ Voice Input")
audio_bytes = st.sidebar.audio_input("Record your voice command")
if audio_bytes:
    st.sidebar.audio(audio_bytes, format="audio/wav")
    st.sidebar.success("🎵 Audio recorded!")
    st.sidebar.info("💡 Add speech_recognition for transcription")

# Quick actions
st.sidebar.markdown("### ⚡ Quick Actions")
if st.sidebar.button("🕐 Current Time"):
    st.session_state.chat_history.append({"role": "assistant", "message": jarvis.get_time()})
    st.rerun()
if st.sidebar.button("📅 Today's Date"):
    st.session_state.chat_history.append({"role": "assistant", "message": jarvis.get_date()})
    st.rerun()
if st.sidebar.button("😄 Tell a Joke"):
    st.session_state.chat_history.append({"role": "assistant", "message": jarvis.tell_joke()})
    st.rerun()
if st.sidebar.button("📝 Show Reminders"):
    st.session_state.chat_history.append({"role": "assistant", "message": jarvis.get_reminders()})
    st.rerun()
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
