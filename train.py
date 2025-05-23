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
            "Use bullet points. Make sure the content is concise, complete, "
            "and fits within 280 characters without looking cut off."
        )
    elif tick_level == "blue tick":
        return (
            f"{user_prompt}\n\n"
            "Use bullet points. Make it a premium, detailed post with professional tone. "
            "Limit content to 2500 characters max, complete without cut offs."
        )
    elif tick_level == "golden tick":
        return (
            f"{user_prompt}\n\n"
            "Use bullet points. Make it very premium, professional, and in-depth. "
            "No character limit. Content should be polished, comprehensive, and complete."
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