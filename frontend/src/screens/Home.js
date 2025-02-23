import './Home.css';
import React, { useEffect, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMicrophone, faCirclePlay, faCircleStop } from '@fortawesome/free-solid-svg-icons';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';

function Home() {
    const { transcript, resetTranscript, browserSupportsSpeechRecognition } = useSpeechRecognition();
    const [listening, setListening] = useState(false);
    const [generatedImages, setGeneratedImages] = useState([]); // Stores multiple images
    const [isLoading, setIsLoading] = useState(false);
    const [lastProcessedText, setLastProcessedText] = useState(""); // Stores last generated text
    const [pauseTimer, setPauseTimer] = useState(null); // Timer to detect pauses

    useEffect(() => {
        if (listening) {
            SpeechRecognition.startListening({ continuous: true });
        } else {
            SpeechRecognition.stopListening();
        }
    }, [listening]);

    useEffect(() => {
        if (listening && transcript.length > lastProcessedText.length) {
            // Reset timer on new speech
            if (pauseTimer) clearTimeout(pauseTimer);

            // Start new timer to detect pause
            setPauseTimer(setTimeout(() => {
                processTranscript(transcript);
            }, 1500)); // ✅ Wait 1.5 seconds after last speech before generating an image
        }
    }, [transcript]);

    const processTranscript = async (text) => {
        if (text.trim() === lastProcessedText.trim()) return; // Avoid duplicate processing
        setLastProcessedText(text.trim()); // ✅ Store last processed sentence
        fetchImageFromTranscript(text.trim());
    };

    const fetchImageFromTranscript = async (text) => {
        setIsLoading(true);
        try {
            const response = await fetch('https://luma-production-15cb.up.railway.app/transcript', {
                mode: 'cors',
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript: text }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Received data:', data);

            if (data.image_url && data.image_url.startsWith("http")) {
                setGeneratedImages(prevImages => [...prevImages, data.image_url]); // ✅ Append new image
            }
        } catch (error) {
            console.error('Error generating image:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleMic = () => {
        if (!listening) {
            resetTranscript();
            setLastProcessedText(""); // Reset last processed sentence
            setListening(true);
        } else {
            setListening(false);
        }
    };

    if (!browserSupportsSpeechRecognition) {
        return <span>Browser doesn't support speech recognition.</span>;
    }

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '100vh', backgroundColor: '#003B53', padding: '20px' }}>
            {/* 🎤 Microphone Button */}
            <button onClick={handleMic} style={{ backgroundColor: '#005B81', border: 'none', padding: 10, borderRadius: '50%' }}>
                <FontAwesomeIcon icon={listening ? faCircleStop : faCirclePlay} color={'#FFFFFF'} size="4x" />
            </button>

            {/* 📜 Display Transcript */}
            <div style={{ marginTop: 20, backgroundColor: 'white', padding: '10px', borderRadius: '10px', minWidth: '50%', textAlign: 'center', fontSize: '18px' }}>
                <p style={{ color: 'black', fontWeight: 'bold' }}>Live Transcript:</p>
                <p style={{ color: '#333' }}>{transcript || "Start speaking..."}</p>
            </div>

            {/* ⏳ Loading Indicator */}
            {isLoading && <p style={{ color: 'white', marginTop: 10 }}>Generating image...</p>}

            {/* 🖼️ Display Latest Image */}
            {generatedImages.length > 0 && (
                <img 
                    src={generatedImages[generatedImages.length - 1]} 
                    alt="Generated from speech"
                    style={{ width: '100%', maxWidth: '500px', height: 'auto', marginTop: 20, borderRadius: '15px' }}
                />
            )}
        </div>
    );
}

export default Home;
