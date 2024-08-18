""" 
Laama Chat - A Streamlit app for chatting with the Llama 3.1 model.
"""
import streamlit as st
import ollama
import base64
import pdfplumber
from docx import Document
from chats_db import create_database, save_chat, load_chats, load_chat_messages, delete_chat
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("laama_chat")

def extract_text(file, file_type):
    """Extract text content from a file based on its MIME type."""
    try:
        if file_type == "application/pdf":
            return extract_text_from_pdf(file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(file)
        elif file_type in ["text/plain", "text/x-python", "text/bat", "text/cmd", "text/sh"]:
            return file.read().decode('utf-8')
        else:
            st.error("Unsupported file type.")
            return ""
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

def extract_text_from_docx(file):
    """Extract text from a DOCX file using python-docx."""
    try:
        doc = Document(file)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return ""

def extract_text_from_pdf(file):
    """Extract text from a PDF file using pdfplumber."""
    try:
        text = ''
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    st.warning("Some pages may not contain extractable text.")
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

def get_ai_response(messages):
    """Get a response from the AI model based on the user messages."""
    try:
        with st.spinner("Laama is thinking..."):
            response = ollama.chat(
                model="llama3.1",
                messages=messages,
            )
        return response['message']['content']
    except Exception as e:
        logger.error(f"Laama response error: {e}")
        return "I'm sorry, I couldn't process your request."

def load_image(image_file):
    """Load an image and convert it to a Base64 string."""
    try:
        with open(image_file, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        logger.error("Background image file not found.")
        return ""

def apply_custom_css(css_file, b64_image, image_ext):
    """Load custom CSS from a file and apply it with a background image."""
    try:
        with open(css_file, "r") as file:
            css = file.read()
        st.markdown(
            f"""
            <style>
            /* Style for the app with background image */
            .stApp {{
                background-image: url('data:image/{image_ext};base64,{b64_image}');
            }}
            {css} /* Custom CSS styles from the styles.css file */
            /* Styles for chat message avatars */
            [data-testid="chatAvatarIcon-user"] {{
                background-color: #42e59e !important;
            }}
            [data-testid="chatAvatarIcon-assistant"] {{
                background-color: #8f3dd0 !important;  /* #aa58e8 */
            }}
            /* Style for sidebar */
            [data-testid="stSidebar"] {{
                background-color: rgba(14, 17, 23, 0.8) !important;
            }}
            /* Style for file uploader */
            [data-testid="stFileUploaderDropzone"] {{
                background-color: rgba(38, 39, 48, 0.6) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        logger.error("CSS file not found.")

def load_saved_chats():
    """Load saved chats from the database."""
    try:
        return load_chats()
    except Exception as e:
        st.error(f"Error loading chats: {e}")
        return []
    
def delete_chat_callback(chat_id, chat_name):
    """Callback function to delete a chat by ID."""
    try:
        delete_chat(chat_id)
        st.session_state.saved_chats = load_saved_chats()
        st.toast(f"Successfully deleted chat ***{chat_name}***.", icon="🗑️")
    except Exception as e:
        st.error(f"Error deleting chat: {e}")

@st.cache_resource
def initialize_database():
    try:
        create_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

def main():
    """Main function for the Laama Chat app."""
    # Set page title and layout
    st.set_page_config(
        page_title="Laama Chat - Llama 3.1",
        page_icon="🦙",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items={
            'About': "# Laama Chat v0.1  \nBy Xyarian 2024  \nhttps://github.com/xyarian  \n\nThis app uses the Llama 3.1 8B model to provide chat responses.  \nhttps://llama.meta.com"
        }
    )
    st.title('Laama Chat')
    st.markdown("Welcome to Laama Chat with Llama 3.1 8.0B! Ask me anything or share a document to get started.")

    # Initialize the database
    initialize_database()

    # Load the background image and convert to Base64
    image_file = "files/bg_image.png"  # Background image file path
    image_ext = "png"  # Background image file extension
    b64_image = load_image(image_file)

    # Apply the custom CSS with the background image
    apply_custom_css("css/styles.css", b64_image, image_ext)

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'saved_chats' not in st.session_state:
        try:
            st.session_state.saved_chats = load_chats()
        except Exception as e:
            st.error(f"Error loading chats: {e}")
            st.session_state.saved_chats = []

    if 'saved_chats' not in st.session_state:
        st.session_state.saved_chats = load_saved_chats()

    # Sidebar with a "New Chat" button
    new_chat_button = st.sidebar.button("🆕 New Chat", help="Start a new chat session")

    # Clear current chat session if the "New Chat" button is clicked
    if new_chat_button:
        st.session_state.messages = []
        st.toast("You can start a new conversation.", icon="✅")
        st.toast("Chat session cleared.", icon="🗑️")

    # Save Chat Button
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Save Your Chats")
    chat_name = st.sidebar.text_input("Enter a chat name:", placeholder="My Chat", max_chars=50)

    if st.sidebar.button("💾 Save Chat", help="Save the current chat session"):
        if chat_name:
            try:
                save_chat(chat_name, st.session_state.messages)
                st.sidebar.success("Chat saved successfully!")
                st.toast(f"Chat ***{chat_name}*** saved successfully.", icon="✅")
                st.session_state.saved_chats = load_chats()
            except Exception as e:
                st.sidebar.error(f"Error saving chat: {e}")
        else:
            st.sidebar.warning("Please enter a chat name before saving.")

    # Saved Chats Section
    st.sidebar.markdown("### Saved Chats")
    for chat_id, chat_name in st.session_state.saved_chats:
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            if st.button(f"{chat_name}", help="Load saved chat", key=f"load_{chat_id}", use_container_width=True):
                try:
                    success, messages = load_chat_messages(chat_id)
                    if success:
                        st.session_state.messages = messages
                        if messages:
                            st.toast(f"Successfully loaded messages for chat ***{chat_name}***.", icon="✅")
                        else:
                            st.toast(f"Chat ***{chat_name}*** has been loaded but contains no messages.", icon="ℹ️")
                except Exception as e:
                    st.error(f"Error loading chat messages: {e}")
        with col2:
            if st.button("❌", help="Delete saved chat", key=f"delete_{chat_id}", on_click=delete_chat_callback, args=(chat_id, chat_name)):
                pass

    # File uploader for adding files to prompts
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "docx", "txt", "bat", "cmd", "sh", "py",])
    if uploaded_file is not None:
        file_content = extract_text(uploaded_file, uploaded_file.type)

        if file_content:
            st.session_state.messages.append({"role": "system", "content": file_content})
            st.success("File content added to context.")
        else:
            st.warning("The file appears to be empty or unreadable.")

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Message Laama Chat..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        ai_response = get_ai_response(st.session_state.messages)
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

if __name__ == "__main__":
    main()
