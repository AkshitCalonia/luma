from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from generate_media import generate_desc, generate_image_url
import os

app = FastAPI()

# Dynamically get the Railway-assigned PORT
PORT = int(os.getenv("PORT", 8000))

# Fix CORS issues by explicitly allowing localhost and production frontend
origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://fastapi-production-cd88.up.railway.app",  # Replace with your new Railway URL
    "https://your-frontend-url.com",  # Replace with your actual frontend URL
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Restrict to known frontend origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check route to confirm FastAPI is running."""
    return {"message": "Hello from FastAPI!"}

# Define the model for receiving transcript data
class TranscriptModel(BaseModel):
    transcript: str

@app.post("/transcript")
async def receive_transcript(transcript: TranscriptModel):
    """Handles transcript processing and image generation."""
    if not transcript.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    print(f"Received transcript: {transcript.transcript}")

    try:
        image_desc = generate_desc(transcript.transcript)
        print("Generated Image Description:", image_desc)

        image_url = generate_image_url(image_desc)
        print("Generated Image URL:", image_url)

        return {"message": image_url}
    except Exception as e:
        print("Error generating image:", str(e))
        raise HTTPException(status_code=500, detail="Error processing transcript.")

@app.post("/titleScreen")
async def create_title_screen(transcript: TranscriptModel):
    """Generates an image based on the provided title screen text."""
    if not transcript.transcript.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty.")

    print(f"Generating title screen for: {transcript.transcript}")

    try:
        image_url = generate_image_url(transcript.transcript)
        print("Title screen image URL:", image_url)

        return {"message": image_url}
    except Exception as e:
        print("Error generating title screen:", str(e))
        raise HTTPException(status_code=500, detail="Error generating title screen.")

# Start the FastAPI server with Railway-compatible dynamic port
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
