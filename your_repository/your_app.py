import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Chatbot Gemini", page_icon="💬")
st.title("💬 Chatbot đơn giản")

# Lấy API key từ Streamlit secrets (đã khai báo ở Advanced settings trên Streamlit Cloud)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

# Khởi tạo lịch sử hội thoại (để chatbot nhớ ngữ cảnh trong phiên chat)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Hiển thị lại toàn bộ tin nhắn cũ mỗi khi trang refresh
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Ô nhập tin nhắn ở cuối trang
prompt = st.chat_input("Nhập tin nhắn...")

if prompt:
    # Hiển thị tin nhắn của người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi tin nhắn tới Gemini và hiển thị phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})