import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
openai_key = os.getenv('OPENAI_API_KEY')

if not openai_key:
    raise ValueError("Missing OpenAI API Key. Make sure OPENAI_API_KEY is set.")

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

def generate_desc(chunk):
    response = client.chat.completions.create(  # <-- FIXED: Using chat.completions.create instead of completions.create
        model="gpt-4",  # Or use "gpt-3.5-turbo" for cheaper costs
        messages=[
            {"role": "system", "content": "You are an assistant that generates concise image prompts."},
            {"role": "user", "content": f"Please condense this text into a 5-word image generation prompt: {chunk}"}
        ],
        max_tokens=50,
        temperature=0.7
    )
    
    image_desc = response.choices[0].message.content.strip()
    print("✅ Debug: Image Description:", image_desc)
    return image_desc



def generate_image_url(image_desc):
  response = client.images.generate(
    model="dall-e-3",
    prompt="children's storybook illustration of a: " + image_desc,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url
  return image_url