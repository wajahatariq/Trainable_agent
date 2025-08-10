import streamlit as st
import json
from litellm import completion

# ---------------------- PAGE SETUP ----------------------
st.set_page_config(page_title="Trainable Agent", page_icon="🤖", layout="centered")
st.title("Trainable Agent")

# ---------------------- SESSION STATE ----------------------
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------- TRAINING FORM ----------------------
st.subheader("Train Your Agent")

with st.form("agent_training_form"):
    agent_name = st.text_input("Agent Name", placeholder="e.g. FitBuddy")
    agent_role = st.text_area("Agent Role / Purpose", placeholder="e.g. You are a fitness coach for busy professionals.")
    agent_tone = st.selectbox("Tone", ["Friendly", "Formal", "Casual", "Sarcastic", "Inspirational"])
    
    st.markdown("**Example Q&A (optional)**")
    example_q1 = st.text_input("Example Question 1", placeholder="e.g. How can I stay fit with a busy schedule?")
    example_a1 = st.text_area("Example Answer 1", placeholder="e.g. Try short HIIT workouts and meal prepping.")
    
    example_q2 = st.text_input("Example Question 2", placeholder="e.g. What's the best healthy snack?")
    example_a2 = st.text_area("Example Answer 2", placeholder="e.g. Nuts, Greek yogurt, or sliced veggies.")
    
    train_button = st.form_submit_button("Train Agent")

if train_button:
    # Build system prompt
    st.session_state.system_prompt = f"""
    You are {agent_name}, {agent_role}.
    Speak in a {agent_tone.lower()} tone.
    
    Example style:
    Q: {example_q1}
    A: {example_a1}
    Q: {example_q2}
    A: {example_a2}
    Follow this style and tone in all responses.
    """
    st.success(f"{agent_name} is trained and ready to chat!")

# ---------------------- CHAT INTERFACE ----------------------
if st.session_state.system_prompt:
    st.subheader("Chat with Your Agent")
    
    user_input = st.text_input("You:", placeholder="Ask your agent something...")
    
    if st.button("Send") and user_input:
        # Append user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Build message payload
        messages = [{"role": "system", "content": st.session_state.system_prompt}]
        messages.extend(st.session_state.chat_history)
        
        try:
            response = completion(
                model="groq/llama3-8b-8192",  # Example Groq model
                messages=messages,
                max_tokens=500
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        
        except Exception as e:
            reply = f"Error: {e}"
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
    
    # Display conversation
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**{agent_name}:** {msg['content']}")

