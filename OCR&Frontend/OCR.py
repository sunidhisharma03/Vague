import streamlit as st
import os
import subprocess
import tempfile
import google.generativeai as genai
from PIL import Image
from transformers import TrOCRProcessor
from optimum.onnxruntime import ORTModelForVision2Seq

# Set page configuration with dark theme
st.set_page_config(
    page_title="Math Visualization Generator", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced dark mode and pop-up overlay
st.markdown("""
    <style>
    /* Dark mode styling */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stTextInput>div>div>input {
        color: #FFFFFF;
        background-color: #262730;
    }
    .stButton>button {
        background-color: #4B8BFF;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #6AA3FF;
        transform: scale(1.05);
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #FFFFFF !important;
    }

    /* Pop-up overlay */
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        color: #FFFFFF;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-size: 24px;
        flex-direction: column;
        text-align: center;
    }
    .spinner {
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-top: 4px solid #fff;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin-bottom: 20px;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
""", unsafe_allow_html=True)

def load_ocr_model():
    """Load the OCR model and processor"""
    processor = TrOCRProcessor.from_pretrained('breezedeus/pix2text-mfr')
    model = ORTModelForVision2Seq.from_pretrained('breezedeus/pix2text-mfr', use_cache=False)
    return processor, model

def extract_text_from_image(image, processor, model):
    """Extract text from the given image"""
    rgb_image = image.convert('RGB')
    pixel_values = processor(images=[rgb_image], return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)
    return generated_text[0] if generated_text else "No text detected"

def generate_manim_code(extracted_text):
    """Generate Manim code based on the extracted text"""
    # Configure Gemini for code generation
    genai.configure(api_key="AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Prompt for Manim code generation
    prompt = f"""
    Generate a comprehensive Manim code visualization for the following quadratic equation or mathematical concept:
    {extracted_text}
    
    Requirements:
    - Create a visually appealing Manim animation
    - Use clear, error-free Python code for the latest Manim version
    - Focus on mathematical visualization
    - Include smooth transitions
    - Use minimal external imports
    - Create a scene that visualizes the mathematical concept
    - Add detailed comments explaining each step of the visualization
    """
    
    response = model.generate_content(prompt)
    return response.text

def save_manim_code(code, filename='try_code/quadratic_visualization.py'):
    """Save the generated Manim code to a file"""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        f.write(code)
    return filename

def run_manim_animation(script_path):
    """
    Run Manim animation and return the path to the generated video
    
    Args:
        script_path (str): Path to the Manim script
    
    Returns:
        str: Path to the generated video file
    """
    try:
        # Create a temporary directory for output
        output_dir = tempfile.mkdtemp()
        
        # Construct Manim command
        command = [
            "manim", 
            "-pql",  # Render in high quality and play the video
            "--media_dir", output_dir,
            script_path
        ]
        
        # Run the command and capture output
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Find the generated video file
        for file in os.listdir(os.path.join(output_dir, "videos")):
            if file.endswith(".mp4"):
                return os.path.join(output_dir, "videos", file)
        
        # If no video found
        st.error("No video generated. Command output:")
        st.text(result.stdout)
        st.text(result.stderr)
        return None
    
    except Exception as e:
        st.error(f"Error running Manim: {str(e)}")
        return None

def main():
    st.title("📸 Math Visualization Creator")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload an image of a mathematical equation...", 
        type=["jpg", "jpeg", "png"],
        help="Upload an image to extract and visualize"
    )
    
    # Load OCR model
    processor, model = load_ocr_model()
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Extract text button
        if st.button("Generate Visualization"):
            with st.spinner('Processing image and generating code...'):
                # Extract text from image
                extracted_text = extract_text_from_image(image, processor, model)
                st.subheader("Extracted Text:")
                st.write(extracted_text)
                
                # Generate Manim code
                try:
                    manim_code = generate_manim_code(extracted_text)
                    
                    # Save the code
                    saved_file = save_manim_code(manim_code)
                    
                    # Annotate code
                    annotated_code = st.text_area(
                        "Edit Manim Code:", 
                        value=manim_code, 
                        height=300
                    )
                    
                    # Run Manim button
                    if st.button("Run Manim Animation"):
                        # Display the overlay pop-up during processing
                        st.markdown("""
                            <div class="overlay">
                                <div class="spinner"></div>
                                <p>Generating your animation... Please wait!</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Save the annotated code
                        with open(saved_file, 'w') as f:
                            f.write(annotated_code)
                        
                        # Run Manim and get video path
                        video_path = run_manim_animation(saved_file)
                        
                        if video_path:
                            # Display the video
                            st.video(video_path)
                            
                            # Download video button
                            with open(video_path, 'rb') as video_file:
                                st.download_button(
                                    label="Download Animation",
                                    data=video_file.read(),
                                    file_name="manim_animation.mp4",
                                    mime="video/mp4"
                                )
                    
                    # Provide download option for code
                    st.download_button(
                        label="Download Manim Code",
                        data=annotated_code,
                        file_name='quadratic_visualization.py',
                        mime='text/python'
                    )
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
