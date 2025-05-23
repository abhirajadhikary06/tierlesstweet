from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("HF_TOKEN")

client = InferenceClient(token=token)

img_description = "Generate an image of an engaging tweet about a project that uses polynomial regression in machine learning. make the post with bulletpoints. make an image for this content"

image = client.text_to_image(img_description)

# 'image' is a PIL Image object, so save it like this:
image.save("generated_image.png")

print("✅ Image saved as generated_image.png")