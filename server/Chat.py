import traceback

import streamlit as st
from streamlit_chat import message

from utils.helper import LLMHelper


def clear_chat_history():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []


def send_msg():
    question = st.session_state['input']
    if question:
        response = llm_helper.generate_response(question, st.session_state['chat_history'])
        st.session_state['chat_history'].append((question, response))
        st.session_state['input'] = ""


try:
    st.set_page_config(layout="wide")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    llm_helper = LLMHelper()

    col1, col2 = st.columns([9, 1])
    with col1:
        st.text_area("You: ", placeholder="请在输入问题时不要透露任何敏感信息，包括个人信息和组织内部信息。", key="input")
    with col2:
        st.text("")
        st.text("")
        st.button("Send", on_click=send_msg)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Clear history", key="clear_history", on_click=clear_chat_history)

    if st.session_state['chat_history']:
        for i in range(len(st.session_state['chat_history']) - 1, -1, -1):
            message(st.session_state['chat_history'][i][1], key=str(i))
            message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
except Exception as e:
    traceback.print_exc()
    st.error(traceback.format_exc())
