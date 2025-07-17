# Cloning API (FastAPI)

This project provides a RESTful API for cloning operations using FastAPI. The API exposes endpoints to perform cloning-related tasks, making it easy to integrate with other applications or automate workflows.

## Features

- FastAPI-based REST API
- Endpoints for cloning operations
- Easy to extend and integrate

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn

Install dependencies:
```bash
pip install -r requirements.txt
```

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

## License

This project is for educational and demonstration purposes.
