import google.generativeai as genai
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("HF_TOKEN")

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

# Function to build the final prompt based on user prompt and tick level
def build_prompt(user_prompt, tick_level):
    if tick_level == "no tick":
        return (
            f"{user_prompt}\n\n"
            "Craft a concise, slightly premium and engaging tweet that conveys the message clearly in under 280 characters. "
            "Avoid complex language and ensure the tweet looks complete, not cut off."
        )
    elif tick_level == "blue tick":
        return (
            f"{user_prompt}\n\n"
            "Write a high-quality, professional tweet thread or post with a polished tone. "
            "Ensure clarity, insight, and completeness within a 2500-character limit. "
            "Maintain a balance between value and readability."
        )
    elif tick_level == "golden tick":
        return (
            f"{user_prompt}\n\n"
            "Create a premium, in-depth, and expertly written post suitable for high-profile or brand-level accounts. "
            "There is no character limit, so focus on delivering comprehensive, authoritative, and refined content that fully explores the topic."
        )
    else:
        return None


# Ask user for their prompt
user_prompt = input("Enter your prompt for content generation:\n").strip()

# Ask user for tick level
tick_level = input("Choose tick level (no tick / blue tick / golden tick): ").strip().lower()

final_prompt = build_prompt(user_prompt, tick_level)

if final_prompt is None:
    print("Invalid tick level! Please choose from: no tick, blue tick, golden tick.")
else:
    response = model.generate_content(final_prompt)
    print(f"\nGenerated content for '{tick_level}':\n")
    print(response.text.strip())

img_prompt = model.generate_content(f'''convert this following prommpt to make an image ... 
                                    
                                    
                                    {user_prompt}''')

client = InferenceClient(token=token)

img_description = img_prompt

image = client.text_to_image(img_description)

# 'image' is a PIL Image object, so save it like this:
image.save("generated_image.png")

print("✅ Image saved as generated_image.png")