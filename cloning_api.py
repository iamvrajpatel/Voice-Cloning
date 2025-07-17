from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
import torch
import soundfile as sf
import os
import uuid
import numpy as np
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from transformers import GPT2Model
from transformers.generation.utils import GenerationMixin

# Setup for TTS
if not issubclass(GPT2Model, GenerationMixin):
    GPT2Model.__bases__ += (GenerationMixin,)

torch.serialization.add_safe_globals([
    XttsConfig,
    XttsAudioConfig,
    BaseDatasetConfig,
    XttsArgs,
])

app = FastAPI(title="Voice Cloning API")

# Global TTS model
device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("Using Device: ", device)
tts = None

@app.on_event("startup")
async def startup_event():
    global tts
    print(f"Loading TTS model on device: {device}")
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False).to(device)
    print("TTS model loaded successfully")

def chunk_text(text, max_length=250):
    sentences = text.split('।')
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk + sentence + '।') <= max_length:
            current_chunk += sentence + '।'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + '।'
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

@app.post("/clone-voice")
async def clone_voice(
    text: str = Form(...),
    language: str = Form(default="hi"),
    reference_audio: UploadFile = File(...)
):
    try:
        unique_id = str(uuid.uuid4())
        ref_audio_path = f"temp_ref_{unique_id}.wav"
        output_path = f"cloned_voice_{unique_id}.wav"
        
        # Save uploaded reference audio
        with open(ref_audio_path, "wb") as f:
            content = await reference_audio.read()
            f.write(content)
        
        # Chunk text if too long
        text_chunks = chunk_text(text)
        audio_chunks = []
        
        # Generate audio for each chunk
        for chunk in text_chunks:
            wav = tts.tts(text=chunk, language=language, speaker_wav=ref_audio_path)
            audio_chunks.append(wav)
        
        # Combine audio chunks
        combined_audio = np.concatenate(audio_chunks)
        
        # Save combined audio
        sf.write(output_path, combined_audio, 24000)
        
        # Clean up temp reference file
        os.remove(ref_audio_path)
        
        return FileResponse(
            path=output_path,
            media_type="audio/wav",
            filename=f"cloned_voice_{unique_id}.wav"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Voice Cloning API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")