import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv('OPENAI_API_KEY')

if not openai_key:
    raise ValueError("Missing OpenAI API Key. Make sure OPENAI_API_KEY is set.")

client = OpenAI(api_key=openai_key)

def generate_desc(chunk):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You generate short, vivid image prompts for children's storybook illustrations. Make them visually detailed but short."},
            {"role": "user", "content": f"Convert this into a concise visual description (5-7 words): {chunk}"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    image_desc = response.choices[0].message.content.strip()
    
    if "cannot proceed" in image_desc.lower():
        raise ValueError("Invalid response received from GPT-4. Adjusting prompt.")
    
    print(" Debug: Image Description:", image_desc)
    return image_desc



def generate_image_url(image_desc):
    response = client.images.generate(
        model="dall-e-3",
        prompt="Children's storybook illustration: " + image_desc,
        size="1024x1024",  
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url
