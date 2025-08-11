import streamlit as st
import datetime
import random
import time
import re

# Page configuration
st.set_page_config(
    page_title="JARVIS AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'commands_count' not in st.session_state:
    st.session_state.commands_count = 0

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #00d4ff;
        font-size: 3em;
        margin-bottom: 20px;
        text-shadow: 0 0 10px #00d4ff;
        font-family: Arial, sans-serif;
    }
    
    .chat-user {
        padding: 10px;
        margin: 5px 0;
        background-color: #2d3748;
        border-radius: 10px;
        border-left: 4px solid #4299e1;
    }
    
    .chat-ai {
        padding: 10px;
        margin: 5px 0;
        background-color: #1a202c;
        border-radius: 10px;
        border-left: 4px solid #00d4ff;
    }
</style>
""", unsafe_allow_html=True)

class JarvisAI:
    def __init__(self):
        self.jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the AI go to therapy? It had too many deep learning issues!",
            "What do you call a computer that sings? A-Dell!",
            "Why don't robots ever panic? They have great artificial composure!"
        ]
        
        self.greetings = [
            "Hello! I'm JARVIS, your AI assistant. How can I help you today?",
            "Greetings! JARVIS at your service. What can I do for you?",
            "Hi there! Ready to assist you with anything you need."
        ]
        
        self.farewells = [
            "Goodbye! Feel free to call on me anytime you need assistance.",
            "See you later! I'll be here whenever you need help.",
            "Until next time! Stay safe and productive."
        ]
    
    def process_command(self, command):
        command_lower = command.lower().strip()
        
        # Greeting
        if any(word in command_lower for word in ["hello", "hi", "hey", "good morning"]):
            return random.choice(self.greetings)
        
        # Time
        elif any(word in command_lower for word in ["time", "what time"]):
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {current_time}"
        
        # Date
        elif any(word in command_lower for word in ["date", "today", "what day"]):
            current_date = datetime.datetime.now().strftime("%B %d, %Y")
            day_of_week = datetime.datetime.now().strftime("%A")
            return f"Today is {day_of_week}, {current_date}"
        
        # Jokes
        elif any(word in command_lower for word in ["joke", "funny", "humor"]):
            return random.choice(self.jokes)
        
        # Math
        elif any(word in command_lower for word in ["calculate", "math", "+", "-", "*", "/"]):
            return self.handle_math(command_lower)
        
        # System status
        elif any(word in command_lower for word in ["system", "status", "info"]):
            return self.get_system_status()
        
        # Weather (demo)
        elif "weather" in command_lower:
            return "It's a perfect day for coding! ☀️ (Weather API integration available in full version)"
        
        # Goodbye
        elif any(word in command_lower for word in ["bye", "goodbye", "see you"]):
            return random.choice(self.farewells)
        
        # Default response
        else:
            return f"I heard you say: '{command}'. I'm still learning! Try asking me about time, date, jokes, or math calculations."
    
    def handle_math(self, command):
        try:
            # Simple math extraction
            numbers_and_ops = re.findall(r'[\d+\-*/().]+', command)
            if numbers_and_ops:
                expression = ''.join(numbers_and_ops)
                # Safety check
                if all(c in '0123456789+-*/(). ' for c in expression):
                    result = eval(expression)
                    return f"The result is: {result}"
            return "I can do math! Try: 'calculate 2 + 2' or '10 * 5'"
        except:
            return "Math error! Try simpler expressions like '2 + 2'"
    
    def get_system_status(self):
        session_time = int(time.time() - st.session_state.start_time)
        return f"""🤖 **JARVIS System Status**

✅ **Status:** Online and Ready
⚡ **Version:** 1.0 Cloud Edition
🕐 **Session Time:** {session_time//60}m {session_time%60}s
💬 **Commands Processed:** {st.session_state.commands_count}
🔥 **All Systems:** Operational

Ready for your next command!"""

# Initialize JARVIS
jarvis = JarvisAI()

def process_user_command(command):
    if command.strip():
        # Add user message
        st.session_state.conversation_history.append({
            'type': 'user',
            'content': command,
            'timestamp': datetime.datetime.now()
        })
        
        # Get AI response
        response = jarvis.process_command(command)
        
        # Add AI response
        st.session_state.conversation_history.append({
            'type': 'ai',
            'content': response,
            'timestamp': datetime.datetime.now()
        })
        
        st.session_state.commands_count += 1
        st.rerun()

# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 JARVIS AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2em; color: #888;">Your Personal AI Assistant</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Control Panel")
        
        # Status
        status = "🟢 Active" if st.session_state.is_listening else "⭐ Ready"
        st.markdown(f"**Status:** {status}")
        
        # Quick stats
        session_time = int(time.time() - st.session_state.start_time)
        st.metric("Session Time", f"{session_time//60}m {session_time%60}s")
        st.metric("Commands", st.session_state.commands_count)
        
        # Voice simulation
        st.subheader("🎤 Voice Mode")
        if st.button("🎙️ Activate Voice"):
            st.session_state.is_listening = True
            st.success("Voice activated!")
            st.rerun()
        
        if st.button("⏹️ Standby"):
            st.session_state.is_listening = False
            st.info("Voice on standby")
            st.rerun()
        
        # Help
        with st.expander("❓ Commands"):
            st.markdown("""
            **Try these:**
            - Hello JARVIS
            - What time is it?
            - Tell me a joke
            - Calculate 25 + 17
            - System status
            - What's the weather?
            """)
    
    # Main chat area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Chat history
        if st.session_state.conversation_history:
            for message in st.session_state.conversation_history[-10:]:
                if message['type'] == 'user':
                    st.markdown(f'<div class="chat-user"><b>👤 You:</b> {message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-ai"><b>🤖 JARVIS:</b> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.info("👋 Say hello to get started!")
        
        # Input
        user_input = st.text_input("Enter your command:", placeholder="Try: Hello JARVIS")
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("📤 Send") and user_input:
                process_user_command(user_input)
        
        with col_b:
            if st.button("🗑️ Clear"):
                st.session_state.conversation_history = []
                st.session_state.commands_count = 0
                st.rerun()
    
    with col2:
        st.subheader("⚡ Quick Commands")
        
        quick_commands = [
            "Hello JARVIS",
            "What time is it?",
            "Tell me a joke",
            "Calculate 10 + 5",
            "System status",
            "What's the weather?",
            "Goodbye"
        ]
        
        for cmd in quick_commands:
            if st.button(cmd, key=f"quick_{cmd}"):
                process_user_command(cmd)

if __name__ == "__main__":
    main()
