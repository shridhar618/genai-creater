# GenAI Creator

A Flask web app for generating AI content (art, music, code and text) from a single prompt, with a saved history of every generation.

## Features

- One prompt interface for four content types: **art**, **music**, **code** and **text**
- Image generation with the OpenAI Images API; text and code generation with OpenAI Chat Completions
- Music mode is a placeholder that suggests music-generation APIs to integrate (Mubert, AIVA, Suno)
- Generation history stored in SQLite (`/history`)
- Download any past generation (`/download/<id>`)

## Tech stack

Python · Flask · Flask-CORS · SQLite · OpenAI API

## Getting started

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
python app.py
```

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| POST | `/generate` | Generate content from a prompt and content type |
| GET | `/history` | List past generations |
| GET | `/download/<id>` | Download a generation |
