import os
import base64
from flask import Flask, request, render_template
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
from datetime import datetime
import re

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
load_dotenv()

# Configure APIs
NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
client = OpenAI(base_url="https://api.studio.nebius.com/v1/", api_key=NEBIUS_API_KEY)

# Function to clean Gemini response (remove markdown symbols)
def clean_response(text):
    # Remove markdown bold (**text**) and headers (# text)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
    text = re.sub(r'#+\s*(.*?)\n', r'\1\n', text)  # Remove # headers
    text = re.sub(r'\n+', ' ', text)  # Replace newlines with spaces
    return text.strip()

# Function to build prompt based on tick level
def build_prompt(user_prompt, tick_level):
    if tick_level == "no tick":
        return (
            f"Based on the keywords: {user_prompt}\n\n"
            "Craft a single, concise, and engaging Twitter post that conveys the message clearly in under 280 characters, including hashtags. "
            "Avoid markdown symbols (e.g., **, # for formatting), complex language, or threads, and ensure the post is complete, not cut off. "
            "Use relevant emojis where appropriate. "
            "Append 2-3 trendy Twitter hashtags relevant to the content."
        )
    elif tick_level == "blue tick":
        return (
            f"Based on the keywords: {user_prompt}\n\n"
            "Write a single, high-quality, professional Twitter post with a polished tone, suitable for a premium account, in under 2500 characters, including hashtags. "
            "Avoid markdown symbols (e.g., **, # for formatting), threads, or cut-off text. "
            "Use relevant emojis sparingly. "
            "Append 2-3 trendy Twitter hashtags relevant to the content."
        )
    elif tick_level == "golden tick":
        return (
            f"Based on the keywords: {user_prompt}\n\n"
            "Create a single, premium, in-depth, and expertly written Twitter post suitable for high-profile or brand-level accounts. "
            "No character limit, but focus on delivering comprehensive, authoritative, and refined content that fully explores the topic. "
            "Avoid markdown symbols (e.g., **, # for formatting), threads, or cut-off text. "
            "Use relevant emojis sparingly. "
            "Append 2-3 trendy Twitter hashtags relevant to the content."
        )
    return None

# Function to generate and save image
def generate_and_save_image(prompt, output_dir="static/generated_images"):
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Generate image using Nebius AI Studio API
        response = client.images.generate(
            model="black-forest-labs/flux-schnell",
            response_format="b64_json",
            extra_body={
                "response_extension": "png",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 4,
                "negative_prompt": "",
                "seed": -1
            },
            prompt=prompt,
        )

        # Extract base64 image data from response
        if not response.data or not response.data[0].b64_json:
            return None, "Error: No image data in response"

        # Decode base64 image data
        image_data = base64.b64decode(response.data[0].b64_json)

        # Save image to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(output_dir, f"generated_image_{timestamp}.png")
        with open(image_path, "wb") as f:
            f.write(image_data)

        # Return relative path for web display
        return os.path.relpath(image_path, "static"), None

    except Exception as e:
        return None, f"Error generating image: {str(e)}"

# Flask route for home page
@app.route("/", methods=["GET", "POST"])
def index():
    content = None
    image_url = None
    error = None

    if request.method == "POST":
        # Get form data
        user_prompt = request.form.get("prompt", "").strip()
        tick_level = request.form.get("tick_level", "").strip().lower()

        # Validate inputs
        if not user_prompt or tick_level not in ["no tick", "blue tick", "golden tick"]:
            error = "Please provide valid keywords and select a tick level (No Tick, Blue Tick, Golden Tick)."
        else:
            # Generate text content
            final_prompt = build_prompt(user_prompt, tick_level)
            if final_prompt is None:
                error = "Invalid tick level selected."
            else:
                try:
                    response = model.generate_content(final_prompt)
                    content = clean_response(response.text.strip())
                    # Generate image using the cleaned content as prompt
                    image_path, image_error = generate_and_save_image(content)
                    if image_path:
                        image_url = f"/static/{image_path}"
                    else:
                        error = image_error
                except Exception as e:
                    error = f"Error generating content: {str(e)}"

    return render_template("index.html", content=content, image_url=image_url, error=error)

if __name__ == "__main__":
    app.run(debug=True)