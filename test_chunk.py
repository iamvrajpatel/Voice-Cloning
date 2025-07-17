import re
import numpy as np
import soundfile as sf
from TTS.api import TTS
import torch

# --- your existing setup ---
torch.serialization.add_safe_globals([
    # ...
])

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print("Using device: ",device)
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    progress_bar=False
).to(device)

speaker_wav = "Narendra_Modi_voice.ogg"
language = "hi"
output_file = "cloned_voice_long.wav"

# --- 1. prepare your long text ---
text = (
    "सबसे पहले......., मैं आपको...... गुजरात के नवसारी में...... स्वागत करता हूँ.......। "
    "यह शहर गुजरात के एक महत्वपूर्ण हिस्से के रूप में जाना जाता है। "
    "यहां के लोग मेहनती हैं और गाँव के जीवन से प्रेम करते हैं। "
    "नवसारी की हवा में एक शांति और सौहार्द्र की भावना है। "
    "यहां के मेले, उत्सव और परंपराएँ लोगों को एक-दूसरे से जोड़कर रखती हैं। "
    "लोग यहां बहुत संवेदनशील और मददगार होते हैं। "
    "जब हम नवसारी आते हैं, तो यह जगह एक घर जैसी लगती है। "
    # imagine you have a much longer paragraph here...
)

# --- 2. chunking function ---
def chunk_text(text, max_chars=200):
    """
    Splits `text` into chunks no longer than max_chars,
    ideally breaking at sentence boundaries.
    """
    # First split into sentences (naïvely on punctuation):
    sentences = re.split(r'(?<=[।!?])\s*', text)
    chunks, current = [], ""
    for sent in sentences:
        if not sent:
            continue
        # If adding this sentence stays under limit, append.
        if len(current) + len(sent) <= max_chars:
            current = (current + " " + sent).strip()
        else:
            # Otherwise, flush current and start new
            if current:
                chunks.append(current)
            # If single sentence too long, break it raw
            if len(sent) > max_chars:
                for i in range(0, len(sent), max_chars):
                    chunks.append(sent[i : i + max_chars])
                current = ""
            else:
                current = sent
    if current:
        chunks.append(current)
    return chunks

# --- 3. synthesize & concatenate ---
chunks = chunk_text(text, max_chars=200)
print(f"Will synthesize {len(chunks)} chunks.")

wav_segments = []
for idx, chunk in enumerate(chunks, 1):
    print(f"  Synthesizing chunk {idx}/{len(chunks)} ({len(chunk)} chars)...")
    wav_chunk = tts.tts(text=chunk, language=language, speaker_wav=speaker_wav)
    wav_segments.append(wav_chunk)

# concatenate numpy arrays
full_wav = np.concatenate(wav_segments, axis=0)

# --- 4. write out ---
sf.write(output_file, full_wav, 24000)
print(f"Long-form voice clone saved to {output_file}")
