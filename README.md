# GenAI Creator

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white) ![OpenAI](https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white)

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

## Environment variables

| Variable | Purpose | Default |
|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for image, text and code generation | placeholder |
| `STABILITY_API_KEY` | Stability AI key, read by `app.py` | placeholder |

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web interface |
| POST | `/generate` | Generate content from a prompt and content type |
| GET | `/history` | List past generations |
| GET | `/download/<id>` | Download a generation |
