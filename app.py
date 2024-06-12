import VertexAI
import PromptGenerator
import os
import subprocess
from manim import *
import google.generativeai as genai
import sys
import webbrowser

# Configure the API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyBYPc0QzXpQ_CJXolJKcUmoiJBWpLUctLE')

def to_markdown(text):
    """Imitate Markdown formatting in console output"""
    print("\nFormatted as Markdown:\n")
    print(text)

def fetch_and_display_content(user_prompt):
    """Fetches both textual explanation and Manim code, then renders and displays video."""
    full_prompt = PromptGenerator.generate_universal_prompt(user_prompt)
    
    # Generate text using the generative AI model
    response = genai.generate_text(prompt=full_prompt)  # Assuming generate_text is the correct method
    print("Raw API Response:", response)  # Debug: Print the raw API response

    # Access the generated text directly from the response object
    textual_content = response.candidates[0]['output'].strip()
    if textual_content:
        to_markdown(textual_content)
    else:
        print("No textual content was found.")

    # Generate Manim code
    manim_code = VertexAI.generate_manim_code(user_prompt)
    print("Manim Code for the topic of ", user_prompt, ":")
    print(manim_code)
    return manim_code

def write_manim_code_to_file(manim_code):
    temp_file = "temp.py"
    with open(temp_file, "w", encoding="utf-8") as f:  # Specify encoding as utf-8
        f.write(manim_code)
    return temp_file

def open_rendered_video(video_file_name):
    try:
        # Specify the path to the rendered video file based on the filename
        video_file_path = os.path.join("media", "videos", "temp", "1080p60", video_file_name)

        # Check if the video file exists
        if os.path.exists(video_file_path):
            # Open the video file using the default system application
            subprocess.Popen(['start', '', video_file_path], shell=True)
            print("Video file opened successfully.")
        else:
            print(f"Video file not found for filename: {video_file_name}")
    except Exception as e:
        print("Error:", e)

def main():
    # Get user input
    user_prompt = input("Enter Topic: ")

    # Generate Manim code based on user input
    manim_code = fetch_and_display_content(user_prompt)

    # Write Manim code to a temporary file
    temp_file = write_manim_code_to_file(manim_code)

    # Specify the name of the video file based on the user input
    video_file_name = f"{user_prompt.lower()}.mp4"

    # Invoke Manim rendering and save the video file with the specified name
    subprocess.run(['manim', temp_file, '-o', video_file_name])

    # Open the rendered video file
    open_rendered_video(video_file_name)

if __name__ == "__main__":
    main()
