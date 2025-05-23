import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="key")

st.title("한톡 (HanTalk) - Korean Chat Tutor")

formality = st.radio("Choose your style:", ["존댓말 (Formal)", "반말 (Casual)"])
user_input = st.text_input("Say something in Korean:")

if "messages" not in st.session_state:
    st.session_state.messages = []

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    if formality == "존댓말 (Formal)":
        system_msg = "You are a helpful Korean tutor. Always reply in polite Korean (존댓말). Speak naturally and clearly for learners."
    else:
        system_msg = "You are a helpful Korean tutor. Always reply in casual Korean (반말). Be friendly, natural, and use simple grammar."

    messages = [{"role": "system", "content": system_msg}] + st.session_state.messages

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
    )

    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**HanTalk:** {msg['content']}")