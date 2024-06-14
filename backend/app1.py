from flask import Flask, request, jsonify, send_from_directory
import os
import subprocess
import VertexAI
import PromptGenerator
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key='AIzaSyBYPc0QzXpQ_CJXolJKcUmoiJBWpLUctLE')

def fetch_and_display_content(user_prompt):
    """Fetches both textual explanation and Manim code, then renders and displays video."""
    full_prompt = PromptGenerator.generate_universal_prompt(user_prompt)
    
    # Generate text using the generative AI model
    response = genai.generate_text(prompt=full_prompt)
    textual_content = response.candidates[0]['output'].strip()

    # Generate Manim code
    manim_code = VertexAI.generate_manim_code(user_prompt)
    return textual_content, manim_code

def write_manim_code_to_file(manim_code):
    temp_file = "temp.py"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(manim_code)
    return temp_file

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        user_prompt = data['prompt']
        
        # Fetch content
        textual_content, manim_code = fetch_and_display_content(user_prompt)
        
        # Write Manim code to file
        temp_file = write_manim_code_to_file(manim_code)
        
        # Generate video filename
        video_file_name = f"{user_prompt.lower()}.mp4"
        
        # Render video with Manim
        subprocess.run(['manim', temp_file, '-o', video_file_name], check=True)
        
        # Return response with text and video filename
        return jsonify({'text': textual_content, 'video': video_file_name})
    except Exception as e:
        app.logger.error('Error: %s', e)
        return jsonify({'error': str(e)}), 500

@app.route('/videos/<filename>')
def get_video(filename):
    return send_from_directory('media/videos/temp/1080p60', filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
