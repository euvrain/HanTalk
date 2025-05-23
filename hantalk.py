import streamlit as st
import subprocess
import re

st.set_page_config(page_title="HanTalk 🦙🇰🇷", layout="centered")
st.title("🦙 HanTalk — Your Chill Korean Tutor")

# Chat history state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("무언가를 한국어로 말해보세요:")

def clean_output(text):
    # Remove terminal color codes
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', text).strip()

def call_llama(prompt):
    llama_path = "/Users/taylormcdonald/llama.cpp/build/bin/llama-simple-chat"
    model_path = "/Users/taylormcdonald/llama.cpp/models/mistral-7b-instruct-v0.1.Q4_0.gguf"

    system_prompt = (
        "너는 한국어를 알려주는 친절하고 귀여운 튜터야. "
        "반말만 쓰고, 자연스럽게 말해. "
        "절대 영어를 쓰지 마. "
        "모르는 단어나 문장이 있으면 '나도 잘 몰라 ㅎㅎ'라고 말해. "
        "짧고 간단하게 대답해줘."
    )

    full_prompt = system_prompt + "\n" + prompt + "\n"

    process = subprocess.Popen(
        [llama_path, "-m", model_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    output, _ = process.communicate(input=full_prompt)

    # Clean terminal color codes
    cleaned = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', output).strip()

    # Remove echoed prompt if present
    if full_prompt in cleaned:
        cleaned = cleaned.split(full_prompt)[-1].strip()

    # Remove repeated lines
    lines = cleaned.splitlines()
    seen = set()
    deduped = []
    for line in lines:
        if line.strip() and line.strip() not in seen:
            seen.add(line.strip())
            deduped.append(line.strip())

    return "\n".join(deduped).strip()

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    with st.spinner("HanTalk 생각중..."):
        reply = call_llama(user_input)
        st.session_state.chat_history.append(("HanTalk", reply))

for speaker, msg in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"🧑‍💻 **You:** {msg}")
    else:
        st.markdown(f"🦙 **HanTalk:** {msg}")