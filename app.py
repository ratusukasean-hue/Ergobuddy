import streamlit as st
from google import genai

st.set_page_config(page_title="ErgoBuddy - Konsultan Ergonomi", page_icon="🪑")
st.title("🪑 ErgoBuddy: AI Konsultan Ergonomi")

# Mengambil API Key secara otomatis dan aman dari Streamlit Secrets
gemini_api_key = st.secrets["GEMINI_API_KEY"]

# Inisialisasi Klien Gemini menggunakan kunci rahasia server
client = genai.Client(api_key=gemini_api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tambahkan tombol Clear Chat di sidebar untuk kenyamanan pengguna publik
if st.sidebar.button("Hapus Riwayat Chat"):
    st.session_state.messages = []
    st.rerun()

# Tampilkan chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Konsultasikan keluhan fisik atau posisi kerjamu di sini..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
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
