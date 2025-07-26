# Cloning API (FastAPI)

This project provides a RESTful API for cloning operations using FastAPI. The API exposes endpoints to perform cloning-related tasks, making it easy to integrate with other applications or automate workflows.

## Features

- FastAPI-based REST API
- Endpoints for cloning operations
- Easy to extend and integrate

## Requirements

- **Python version:** 3.11.9  
  Make sure you have Python 3.11.9 installed. You can download it from [python.org](https://www.python.org/downloads/release/python-3119/).

## Installation

1. **Set up a virtual environment** (recommended):

   ```sh
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Clone the repository** (if applicable):

   ```sh
   git clone https://github.com/iamvrajpatel/Voice-Cloning.git
   cd Voice-Cloning
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

   If you need development or extra dependencies, check for additional requirements files or documentation.

## Running the API

To start the API server, run:
```bash
uvicorn cloning_api:app --port 8000 --host 0.0.0.0
```
- `cloning_api.py` should be in the project root
- The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Usage

- Access the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
- Use the provided endpoints to perform cloning operations.

### Example: Clone Voice Using `curl`

```bash
curl --location 'http://localhost:8000/clone-voice' \
--form 'text="एक बार की बात है एक राजा था। उसका एक बड़ा-सा राज्य था। एक दिन उसे देश घूमने का विचार आया और उसने देश भ्रमण की योजना बनाई और घूमने निकल पड़ा। जब वह यात्रा से लौट कर अपने महल आया। उसने अपने मंत्रियों से पैरों में दर्द होने की शिकायत की। राजा का कहना था कि मार्ग में जो कंकड़ पत्थर थे वे मेरे पैरों में चुभ गए और इसके लिए कुछ इंतजाम करना चाहिए।"' \
--form 'language="hi"' \
--form 'reference_audio=@"D:/Python/dia1.6/Narendra_Modi_voice.ogg"'
```

- Replace the `reference_audio` path with your own reference audio file.
- The response will be a WAV file containing the cloned voice.

## Project Structure

- `cloning_api.py`: Main FastAPI application with cloning endpoints.
- `README.md`: Documentation and usage instructions.

## Used Configuration of GPU
- [Used RunPod Configuration](https://console.runpod.io/deploy?gpu=RTX%20A4500&count=1&template=runpod-torch-v280)

## License

This project is for educational and demonstration purposes.
