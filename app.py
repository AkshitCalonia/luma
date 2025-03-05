from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from generate_media import generate_desc, generate_image_url
import os

app = FastAPI()

# connct this thing to railway , 
PORT = int(os.getenv("PORT", 8080))

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://fastapi-production-cd88.up.railway.app", 
    "https://your-frontend-url.com",  
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

class TranscriptModel(BaseModel):
    transcript: str

@app.post("/transcript")
async def receive_transcript(transcript: TranscriptModel):
    if not transcript.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty.")

    print(f"Received transcript: {transcript.transcript}")

    try:
        image_desc = generate_desc(transcript.transcript)
        print("Generated Image Description:", image_desc)

        image_url = generate_image_url(image_desc)
        print("Generated Image URL:", image_url)

        return {"image_url": image_url}  
    except Exception as e:
        print("Error generating image:", str(e))
        raise HTTPException(status_code=500, detail="Error processing transcript.")


@app.post("/titleScreen")
async def create_title_screen(transcript: TranscriptModel):
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
