# # import requests

# # # Replace with your actual API key and Gemini base URL
# # # API_KEY = "AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M"
# # import os
# # import google.generativeai as genai

# # # Set up your API key
# # os.environ["GEMINI_API_KEY"] = "AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M"  # Replace with your actual API key

# # # Configure the GenAI client
# # genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# # # Generate a simple response
# # response = genai.generate_text(
# #     model="gemini-1.5-flash",
# #     prompt="Explain what quadratic equations are in simple terms.",
# #     max_output_tokens=200,
# #     temperature=0.7,
# # )

# # # Print the response
# # print(response["text"])
# import os
# import google.generativeai as genai

# # Set your API key
# os.environ["GEMINI_API_KEY"] = "AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M"  # Replace with your actual API key

# # Configure the GenAI client
# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# # Generate a response (example based on typical structure)
# response = genai.generate(
#     model="gemini-1.5-flash",
#     prompt="What is a quadratic equation?",
#     max_output_tokens=200,
#     temperature=0.7,
# )

# # Print the generated response
# print(response.get("text", "No response text available."))
import google.generativeai as genai

genai.configure(api_key="AIzaSyA77m7xbz716FY9eaxo-Rmo087_xNKs33M")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Give me error free code only in manim for visualizing in graph how the solution of a quadratic equation is calculated. Make it visually appealing and comprehensive as possible with proper management of screen and transitions.")
print(response.text)




