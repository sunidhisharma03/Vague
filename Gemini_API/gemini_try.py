# import re
# import google.generativeai as genai
# import subprocess
# import os

# # Configure the Google Gemini API
# genai.configure(api_key="AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M")
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Function to extract Python code from the response
# def extract_python_code(text):
#     code_pattern = r"```python\n(.*?)```"
#     matches = re.findall(code_pattern, text, re.DOTALL)
#     return "\n".join(matches)

# # Function to save code to a Python file
# def save_code_to_file(code, filename="generated_manim_code.py"):
#     with open(filename, "w") as file:
#         file.write(code)

# # Function to execute Manim code
# def execute_manim_script(filename, output_dir="output"):
#     try:
#         os.makedirs(output_dir, exist_ok=True)
#         command = f"manim {filename} -o {output_dir} --quality h"
#         subprocess.run(command, check=True, shell=True)
#         print(f"Animation successfully generated in {output_dir}/")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Error during Manim execution: {e}")
#         return False

# # Function to validate and sanitize code
# def validate_code(code):
#     # Add necessary imports if missing
#     required_imports = ["from manim import *", "import math", "import numpy as np"]
#     for req in required_imports:
#         if req not in code:
#             code = f"{req}\n" + code
    
#     # Remove potentially malformed LaTeX directives
#     code = re.sub(r"\\usepackage{.*?}", "", code)
    
#     # Add LaTeX configuration safely for Manim
#     if "\\documentclass" not in code:
#         latex_setup = r"""
# # Ensure LaTeX packages are added via Manim configuration
# from manim import config
# config["tex_template"].add_to_preamble(r'''
# \usepackage{amsmath}
# \usepackage{gensymb}
# \usepackage{amssymb}
# ''')
# """
#         code = latex_setup + "\n" + code
#     return code

# # Function to refine and retry failed code
# def refine_and_retry(error_message, current_code, attempt):
#     error_context = f"""
#     Attempt {attempt}:
#     Manim execution failed due to the following error:
#     {error_message}

#     Refine the code below to resolve the issue:
#     {current_code}

#     Ensure:
#     1. Text and animations are positioned clearly using methods like `.to_edge()`, `.align_to()`, and `.shift()`.
#     2. Avoid overlapping elements by adjusting their positions dynamically.
#     3. Animations should appear sequentially and not obscure each other.
#     4. Labels, equations, and visuals should be properly aligned for clarity.
#     5. The Manim Scene structure is correctly defined.

#     Provide only the refined Python code.
#     """
#     response = model.generate_content(error_context)
#     return extract_python_code(response.text)

# # Function to test and run the extracted code
# def test_and_run_code(code, max_retries=12):
#     filename = "generated_manim_code.py"
#     for attempt in range(max_retries):
#         try:
#             # Validate and sanitize the code
#             code = validate_code(code)
#             # Save the code to a file
#             save_code_to_file(code, filename)
#             # Attempt to execute the Manim script
#             success = execute_manim_script(filename)
#             if success:
#                 print(f"Code executed successfully on attempt {attempt + 1}.")
#                 break
#         except Exception as e:
#             error_message = str(e)
#             print(f"Error encountered on attempt {attempt + 1}: {error_message}")
#             if attempt + 1 < max_retries:
#                 code = refine_and_retry(error_message, code, attempt + 1)
#             else:
#                 print("Maximum retries reached. Could not execute code successfully.")
#                 print("Last attempted code:")
#                 print(code)

# # Prompt user for a physics or math topic
# topic = input("Enter a physics or math topic to animate (e.g., Projectile Motion, Fourier Transform): ")

# # Generate a prompt for Google Gemini
# prompt = f"""
# Generate Python code using Manim to animate and explain "{topic}" in a 3Blue1Brown style.
# Ensure:
# 1. All necessary imports (`manim`, `math`, `numpy`) are included.
# 2. LaTeX setup is valid and compatible with Manim's configuration.
# 3. The animation lasts at least 25 seconds.
# 4. Avoid overlapping visuals by positioning elements dynamically using `.to_edge()`, `.align_to()`, `.shift()`, and similar methods.
# 5. Place text and objects to maximize clarity and minimize visual clutter.
# 6. Animate elements sequentially to ensure clear transitions between scenes.
# 7. Include labels, equations, and diagrams that are aligned and legible.
# 8. Use modular code design for scalability and reusability.

# Provide only the Python code.
# """

# # Generate initial code from Google Gemini
# response = model.generate_content(prompt)
# generated_code = extract_python_code(response.text)

# # Display the generated code for debugging
# print("Generated Python Code:")
# print(generated_code)

# # Test and run the extracted code
# test_and_run_code(generated_code)

import re
import google.generativeai as genai
import subprocess
import os
from manim import config
from manim import *

# Configure the Google Gemini API
genai.configure(api_key="AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M")
model = genai.GenerativeModel("gemini-1.5-flash")

# Configure LaTeX preamble for Manim
config["tex_template"].add_to_preamble(r"""
\usepackage{amsmath}
\usepackage{gensymb}
\usepackage{amssymb}
""")

# Function to extract Python code from the response
def extract_python_code(text):
    code_pattern = r"```python\n(.*?)```"
    matches = re.findall(code_pattern, text, re.DOTALL)
    return "\n".join(matches)

# Function to save code to a Python file
def save_code_to_file(code, filename="generated_manim_code.py"):
    with open(filename, "w") as file:
        file.write(code)

# Function to execute Manim code and play animation
def execute_manim_script(filename, output_dir="output"):
    try:
        os.makedirs(output_dir, exist_ok=True)
        check_latex_configuration()
        command = f"manim {filename} -o {output_dir} --quality h"
        subprocess.run(command, check=True, shell=True)
        print(f"Animation successfully generated in {output_dir}/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Execution failed: {e}")
        if "LaTeX" in str(e):
            print("LaTeX-related error detected. Verify your LaTeX installation and packages.")
        return False
    except Exception as e:
        print(f"Unexpected error during execution: {e}")
        return False

# Function to check LaTeX configuration
def check_latex_configuration():
    try:
        subprocess.run(["latex", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("LaTeX installation verified.")
        required_packages = ["amsmath", "gensymb", "amssymb"]
        for package in required_packages:
            if not subprocess.run(["kpsewhich", f"{package}.sty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout:
                raise RuntimeError(f"Missing LaTeX package: {package}")
        print("All required LaTeX packages are installed.")
    except subprocess.CalledProcessError:
        raise RuntimeError("LaTeX is not installed or misconfigured. Please verify your setup.")

# Function to validate and enhance the code
def validate_code(code):
    required_imports = ["from manim import *", "import math", "import numpy as np"]
    for req in required_imports:
        if req not in code:
            code = f"{req}\n" + code
    return code

# Function to refine code multiple times
def refine_code_multiple_times(initial_code, num_refinements=3):
    code = initial_code
    for i in range(1, num_refinements + 1):
        refinement_prompt = f"""
        Refine the Python code below to generate a Manim animation:
        {code}
        
        Ensure:
        1. No overlapping text or visuals; use `.to_edge()`, `.shift()`, etc.
        2. Smooth animations with appropriate timing.
        3. Legible, aligned, and dynamically spaced elements.
        4. Modular code with reusable components.
        5. Compatibility with LaTeX setup and proper LaTeX commands.
        6. A runtime of at least 25 seconds.

        Provide only the refined Python code.
        """
        response = model.generate_content(refinement_prompt)
        code = extract_python_code(response.text)
    return code

# Function to test, refine, and run the animation code
def test_refine_and_animate(code, max_retries=12):
    filename = "generated_manim_code.py"
    for attempt in range(max_retries):
        try:
            code = validate_code(code)
            save_code_to_file(code, filename)
            if execute_manim_script(filename):
                print("Animation generated and played successfully.")
                return
            else:
                print(f"Execution failed on attempt {attempt + 1}. Retrying...")
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")

        refinement_prompt = f"""
        The previous code failed with error: {e}
        Refine the code below to fix the issue and improve visualization:

        {code}

        Ensure all issues are resolved and provide error-free Python code.
        """
        response = model.generate_content(refinement_prompt)
        code = extract_python_code(response.text)
    print("Maximum retries reached. Could not execute code successfully.")
    print("Final code attempt:")
    print(code)

# Main prompt to generate animation code
topic = input("Enter a topic to animate (e.g., Projectile Motion, Fourier Transform): ")
prompt = f"""
Generate Python code using Manim to animate and explain "{topic}" in a 3Blue1Brown style.
Ensure:
1. All necessary imports (`manim`, `math`, `numpy`) are included.
2. LaTeX setup is valid and compatible with Manim's configuration.
3. Avoid overlapping visuals by positioning elements using `.to_edge()`, `.shift()`, `.align_to()`, etc.
4. Use smooth transitions and dynamic spacing for clarity.
5. Include modular code design for scalability.
6. Animation duration must be at least 25 seconds.

Provide only the Python code.
"""

# Generate, refine, and run the animation code
response = model.generate_content(prompt)
initial_code = extract_python_code(response.text)
refined_code = refine_code_multiple_times(initial_code)
print("Refined Code:")
print(refined_code)
test_refine_and_animate(refined_code)



# import re
# import google.generativeai as genai
# import subprocess
# import os
# from manim import config
# from manim import *

# # Configure the Google Gemini API
# genai.configure(api_key="AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M")
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Configure LaTeX preamble for Manim
# config["tex_template"].add_to_preamble(r"""
# \usepackage{amsmath}
# \usepackage{gensymb}
# \usepackage{amssymb}
# """)

# def extract_python_code(text):
#     """Extract Python code from text response."""
#     code_pattern = r"```python\n(.*?)```"
#     matches = re.findall(code_pattern, text, re.DOTALL)
#     return "\n".join(matches)

# def save_code_to_file(code, filename="generated_manim_code.py"):
#     """Save generated Python code to a file."""
#     with open(filename, "w") as file:
#         file.write(code)

# def execute_manim_script(filename, output_dir="output"):
#     """Run Manim script and handle errors."""
#     try:
#         os.makedirs(output_dir, exist_ok=True)
#         check_latex_configuration()
#         command = f"manim {filename} -o {output_dir} --quality h"
#         subprocess.run(command, check=True, shell=True)
#         print(f"Animation successfully generated in {output_dir}/")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f"Error during Manim execution: {e}")
#         return False

# def check_latex_configuration():
#     """Ensure LaTeX and required packages are installed."""
#     try:
#         subprocess.run(["latex", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         required_packages = ["amsmath", "gensymb", "amssymb"]
#         for package in required_packages:
#             if not subprocess.run(["kpsewhich", f"{package}.sty"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout:
#                 raise RuntimeError(f"Missing LaTeX package: {package}")
#     except subprocess.CalledProcessError:
#         raise RuntimeError("LaTeX is required but not installed or misconfigured.")

# def validate_code(code):
#     """Add essential imports if missing."""
#     required_imports = ["from manim import *", "import math", "import numpy as np"]
#     for req in required_imports:
#         if req not in code:
#             code = f"{req}\n" + code
#     return code

# def refine_code_multiple_times(initial_code, num_refinements=3):
#     """Iteratively refine the generated code."""
#     code = initial_code
#     for i in range(1, num_refinements + 1):
#         prompt = f"""
#         Improve the Python code for a Manim animation:

#         {code}

#         Ensure clarity, proper transitions, modular design, and no overlaps in visuals.
#         """
#         response = model.generate_content(prompt)
#         code = extract_python_code(response.text)
#     return code

# def test_refine_and_animate(code, max_retries=5):
#     """Refine and run the code, retrying upon failure."""
#     filename = "generated_manim_code.py"
#     for attempt in range(max_retries):
#         try:
#             code = validate_code(code)
#             save_code_to_file(code, filename)
#             if execute_manim_script(filename):
#                 print("Animation generated successfully.")
#                 return
#         except Exception as e:
#             error_message = str(e)
#             print(f"Error on attempt {attempt + 1}: {error_message}")

#             prompt = f"""
#             The previous code failed with the error:
#             {error_message}

#             Refine the code below to fix the issue and improve the animation:
#             {code}
#             """
#             response = model.generate_content(prompt)
#             code = extract_python_code(response.text)
#     print("Maximum retries reached. Could not execute the code.")

# # Prompt user for a topic
# topic = input("Enter a physics or math topic to animate (e.g., Projectile Motion, Fourier Transform): ").strip()

# if not topic:
#     print("Error: Topic cannot be empty.")
#     exit()

# # Generate prompt for Gemini AI
# prompt = f"""
# Generate Python code for a Manim animation to explain "{topic}" in a 3Blue1Brown style.
# Include:
# 1. Text, visuals, and animations for clarity.
# 2. Properly aligned and legible objects.
# 3. A duration of at least 25 seconds.
# """

# response = model.generate_content(prompt)
# initial_code = extract_python_code(response.text)

# # Refine and run the animation
# refined_code = refine_code_multiple_times(initial_code)
# test_refine_and_animate(refined_code)
