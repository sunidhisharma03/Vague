import streamlit as st
import base64

def get_base64_of_bin_file(bin_file):
    """Reads a binary file and returns its base64 encoded string.

    Args:
        bin_file (str): Path to the binary file.

    Returns:
        str: Base64 encoded string of the file content.
    """

    try:
        with open(bin_file, 'rb') as file:
            return base64.b64encode(file.read()).decode()
    except Exception as e:
        st.error(f"Error loading background video: {e}")
        return ""

def set_page_config():
    """Sets the page configuration for the Streamlit app."""

    st.set_page_config(
        page_title="VIZMath",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="collapsed"  # Hide the sidebar initially
    )

def set_bg_video(video_file):
    """Sets the video background for the Streamlit app.

    Args:
        video_file (str): Path to the video file.
    """

    video_base64 = get_base64_of_bin_file(video_file)

    video_css = f"""
    <style>
        .stApp {{
            background-color: transparent;
        }}
        .video-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            z-index: -1;
        }}
        .home-container {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            color: white;
        }}
        .title {{
            font-size: 6rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
        }}
        .start-button {{
            padding: 15px 30px;
            font-size: 1.5rem;
            background-color: black;
            color: white;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .start-button:hover {{
            background-color: #333;
            color: white;
        }}
    </style>

    <video autoplay muted loop class="video-background">
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    """

    st.markdown(video_css, unsafe_allow_html=True)

def home_page():
    """Renders the home page of the app."""

    set_page_config()
    set_bg_video("Smallgirl.mp4")  # Replace with your video file

    st.markdown('<div class="home-container">', unsafe_allow_html=True)
    st.markdown('<div class="title">VIZMath</div>', unsafe_allow_html=True)

    if st.button("Start with VIZ", key="start_button"):
        st.experimental_set_query_params(page="main")  # Navigate to the second page

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    home_page()