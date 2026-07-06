import streamlit as st
from google import genai

st.set_page_config(page_title="ErgoBuddy - Konsultan Ergonomi", page_icon="🪑")
st.title("🪑 ErgoBuddy: AI Konsultan Ergonomi")

# Input API Key Gemini di Sidebar
gemini_api_key = st.sidebar.text_input("Masukkan Google Gemini API Key", type="password")

if not gemini_api_key:
    st.info("Silakan masukkan Gemini API Key di sidebar untuk mulai berkonsultasi.", icon="🔑")
else:
    # Inisialisasi Klien Gemini
    client = genai.Client(api_key=gemini_api_key)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Konsultasikan keluhan fisik atau posisi kerjamu di sini..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            # Gunakan instruksi use case ergonomi untuk Gemini
            system_instruction = (
                "Anda adalah ErgoBuddy, asisten AI pakar Teknik Industri bidang Ergonomi dan K3. "
                "Tugas Anda adalah membantu memberikan solusi mengenai posisi kerja, penataan stasiun kerja, "
                "pencegahan cedera fisik, dan memberikan tips peregangan singkat yang ramah."
            )
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3
                )
            )
            st.markdown(response.text)
            
        st.session_state.messages.append({"role": "assistant", "content": response.text})
