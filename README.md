# 🎭 Spotify Alter Ego

This Flask web app creates a **Pixar-style character** based on your Spotify listening history using:

- 🎵 Spotify Web API (via Spotipy)
- 🤖 Ollama + Llama3 for character description
- 🎨 Stable Diffusion (Dreamshaper) for image generation
- 💻 Local image API exposed via ngrok
- 🧠 Animated frontend built with Tailwind CSS

---

## 🚀 Features

- Log in with Spotify to fetch your top and recent tracks
- Generate a unique character description using Ollama (Llama3)
- Create a Pixar-style cartoon portrait using Stable Diffusion
- Works on CPU with secure local image server

**Not Public - Spotify Developer update

---

## 🧠 Tech Stack

| Component        | Stack                         |
|------------------|-------------------------------|
| Backend          | Flask                         |
| Spotify API      | Spotipy                       |
| Language Model   | Ollama (Llama3)               |
| Image Generation | Hugging Face + Diffusers      |
| Frontend         | HTML + Tailwind CSS           |
| Tunnel           | Ngrok                         |
| Secrets          | `.env` + python-dotenv        |

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/spotify-avatar-generator.git
cd spotify-avatar-generator
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```


2. Create a .env file in the root directory:
```bash
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
FLASK_SECRET_KEY=some_random_string
HUGGINGFACE_TOKEN=your_huggingface_token
```

3. Make sure you're logged in to Ollama and have the llama3 model installed:
```bash
ollama run llama3
```
4. Open your browser to http://localhost:5000/ui
5. 
---
## 🔑 How to Get Spotify API Keys

1. To use the Spotify API, you’ll need to register your own app and get credentials:

2. Go to the Spotify Developer Dashboard.

3. Log in and click "Create an App".

4. Give it a name and description (anything is fine).

5. Once created, you'll see your Client ID and Client Secret — copy these into your .env file.

6. Click "Edit Settings" and add your Redirect URI:
```bash
http://localhost:5000/callback
```
7. Save settings and add keys to .env file.

---
## 🤖 Credits
Spotify Web API

Ollama

Diffusers + DreamShaper LoRA

Inspired by Pixar, memes, and late-night energy ⚡

ChatGPT 
