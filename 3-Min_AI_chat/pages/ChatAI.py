import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


st.set_page_config("Чат с ИИ", layout="wide")


st.title("Чат с ИИ")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def stream_text(text: str):
    for char in text:
        yield char
        time.sleep(0.03)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


if "token_stats" not in st.session_state:
    st.session_state.token_stats = {}


with st.sidebar:
    st.header("Настройки")
    system_prompt = st.text_area(
        "Пользовательский промпт",
        value="Ты полезный ИИ-ассистент. Отвечай понятно и кратко.",
        height=200,
    )

    st.header("Токены")
    st.json(st.session_state.token_stats)


messages = st.container(height=600)


for msg in st.session_state.chat_history:
    messages.chat_message(msg["role"]).write(msg["content"])


req = st.chat_input("Скажите что-нибудь?")


if req:
    user_msg = {
        "role": "user",
        "content": req,
    }
    st.session_state.chat_history.append(user_msg)
    messages.chat_message("user").write(req)


    ai_messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ] + st.session_state.chat_history


    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=ai_messages,
    )


    assistant_text = completion.choices[0].message.content


    if completion.usage:
        st.session_state.token_stats = completion.usage.model_dump()


    with messages.chat_message("assistant"):
        streamed_text = st.write_stream(stream_text(assistant_text))


    assistant_msg = {
        "role": "assistant",
        "content": streamed_text,
    }
    st.session_state.chat_history.append(assistant_msg)


    st.rerun()