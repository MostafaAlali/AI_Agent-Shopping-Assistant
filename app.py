import os
import streamlit as st
from shopping_agent import agent

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="AI Shopping Agent",
    page_icon="🛒",
    layout="centered"
)

# Create a temporary directory for image uploads if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp_uploads")
os.makedirs(TEMP_DIR, exist_ok=True)

# --- 2. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! What are you looking to buy today? You can type a request or upload a photo in the sidebar!"}
    ]

# Track uploaded files so we don't re-process the same image on every Streamlit rerun
if "processed_images" not in st.session_state:
    st.session_state.processed_images = set()

# --- 3. Sidebar for Visual Tools ---
with st.sidebar:
    st.header("📸 Visual Search")
    st.markdown("Upload a picture of a product to find it in our store.")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

# --- 4. Main Chat Interface ---
st.title("🛒 AI Shopping Assistant")

# Render existing conversation history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # If the message contains an image path, render the image in the chat
        if "image_path" in msg:
            st.image(msg["image_path"], width=200)
        
        # Hide the system-level image prompt from the user UI for a cleaner experience
        if msg["content"] and not msg["content"].startswith("SYSTEM_IMAGE_TRIGGER:"):
            st.markdown(msg["content"])
        elif msg["content"].startswith("SYSTEM_IMAGE_TRIGGER:"):
            st.markdown("*(Analyzed uploaded image)*")

# --- 5. Input Handling (Text or Image) ---
user_input = st.chat_input("e.g., I want to buy an organic apple...")

trigger_text = None
display_text = None
image_path_to_save = None

# Scenario A: User uploaded a new image
if uploaded_file and uploaded_file.name not in st.session_state.processed_images:
    st.session_state.processed_images.add(uploaded_file.name)
    
    # Save file locally so the backend vision tool can access it via path
    file_path = os.path.join(TEMP_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Set up the hidden trigger for the LLM and the clean display text for the UI
    trigger_text = f"SYSTEM_IMAGE_TRIGGER: I uploaded an image at {file_path}. Please identify it using describe_prduct_image and search for it."
    display_text = "*(Analyzing uploaded image...)*"
    image_path_to_save = file_path

# Scenario B: User typed a text message 
elif user_input:
    trigger_text = user_input
    display_text = user_input

# --- 6. Agent Invocation Pipeline ---
if trigger_text:
    # Append the new interaction to the session state
    new_msg = {"role": "user", "content": trigger_text}
    if image_path_to_save:
        new_msg["image_path"] = image_path_to_save
    st.session_state.messages.append(new_msg)

    # Immediately render the user's action in the UI
    with st.chat_message("user"):
        if image_path_to_save:
            st.image(image_path_to_save, width=200)
        st.markdown(display_text)

    # Process with the LangChain agent
    with st.spinner("Processing..."):
        try:
            # Data Sanitization: Strip out custom UI keys (like 'image_path') 
            # LangChain strictly expects standard 'role' and 'content' dictionaries
            clean_messages = [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages
            ]
            
            result = agent.invoke({"messages": clean_messages})
            
            # Extract the final response safely
            final_message = result["messages"][-1]
            bot_reply = final_message.content if hasattr(final_message, 'content') else final_message["content"]
        
        except Exception as e:
            bot_reply = f"**System Error:** {str(e)}"

    # Render and save the assistant's response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    
    # Force a rerun to stabilize the UI state, especially after a sidebar interaction
    st.rerun()