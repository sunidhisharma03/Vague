import streamlit as st
import pytesseract
import google.generativeai as genai
from PIL import Image
import os
import subprocess
import tempfile

def load_gemini_model():
    """Configure and load Gemini model for code generation"""
    genai.configure(api_key="AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M")
    return genai.GenerativeModel("gemini-1.5-flash")

def process_uploaded_file(uploaded_file):
    """Process the uploaded image using OCR."""
    try:
        image = Image.open(uploaded_file)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return None

def generate_manim_code(prompt):
    """Generate Manim code based on the user's prompt"""
    model = load_gemini_model()
    
    full_prompt = f"""
    Generate a comprehensive Manim code visualization for the following mathematical concept:
    {prompt}
    
    Requirements:
    - Create a visually appealing Manim animation
    - Use clear, error-free Python code for the latest Manim version
    - Focus on mathematical visualization
    - Include smooth transitions
    - Use minimal external imports
    - Create a scene that visualizes the mathematical concept
    - Add detailed comments explaining each step of the visualization
    """
    
    response = model.generate_content(full_prompt)
    return response.text

def save_manim_code(code, filename='manim_code/animation.py'):
    """Save the generated Manim code to a file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write(code)
    return filename

def run_manim_animation(script_path):
    """Run Manim animation and return the path to the generated video"""
    try:
        output_dir = tempfile.mkdtemp()
        
        command = [
            "manim", 
            "-pql",  # Render in high quality and play the video
            "--media_dir", output_dir,
            script_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        for file in os.listdir(os.path.join(output_dir, "videos")):
            if file.endswith(".mp4"):
                return os.path.join(output_dir, "videos", file)
        
        st.error("No video generated. Command output:")
        st.text(result.stdout)
        st.text(result.stderr)
        return None
    
    except Exception as e:
        st.error(f"Error running Manim: {str(e)}")
        return None

def main():
    # Set page configuration
    st.set_page_config(page_title="Manim Animation Generator", page_icon="🎨", layout="wide")
    
    # Navbar-like header
    st.markdown("""
    <div style="
        background-color: #f8f9fa; 
        padding: 10px 20px; 
        border-bottom: 1px solid #e0e0e0; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    ">
        <div style="font-size: 1.5rem; font-weight: bold;">🎨 Manim Animation Generator</div>
        <div>
            <a href="#" style="margin-right: 15px; color: #007bff; text-decoration: none;">Home</a>
            <a href="#" style="margin-right: 15px; color: #007bff; text-decoration: none;">About</a>
            <a href="#" style="color: #007bff; text-decoration: none;">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content container
    st.markdown('<div style="padding: 20px; background-color: white;">', unsafe_allow_html=True)
    
    # Input method selection
    input_method = st.selectbox(
        "Choose your input method", 
        ["Text Prompt", "Image OCR"],
        index=0
    )
    
    # Chat history initialization
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input section based on selected method
    prompt = None
    if input_method == "Text Prompt":
        prompt = st.chat_input("Describe the animation you want to create")
    else:  # Image OCR
        uploaded_file = st.file_uploader("Upload an image for OCR", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            extracted_text = process_uploaded_file(uploaded_file)
            if extracted_text:
                st.success("OCR extraction successful!")
                st.write("Extracted text:")
                st.text(extracted_text)
                prompt = extracted_text
    
    # Process the input
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate Manim code
        with st.chat_message("assistant"):
            with st.spinner("Generating Manim code..."):
                try:
                    manim_code = generate_manim_code(prompt)
                    
                    # Display generated code
                    st.code(manim_code, language="python")
                    
                    # Save code to file
                    saved_file = save_manim_code(manim_code)
                    
                    # Editable code area
                    edited_code = st.text_area("Edit Manim Code", value=manim_code, height=300)
                    
                    # Animation generation buttons
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Generate Animation", type="primary"):
                            with st.spinner("Rendering animation..."):
                                # Save edited code
                                with open(saved_file, 'w') as f:
                                    f.write(edited_code)
                                
                                # Run Manim and get video path
                                video_path = run_manim_animation(saved_file)
                                
                                if video_path:
                                    st.video(video_path)
                    
                    with col2:
                        st.download_button(
                            label="Download Manim Code",
                            data=edited_code,
                            file_name="manim_animation.py",
                            mime="text/python"
                        )
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": "Generated Manim code"})
    
    # Close main content container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()