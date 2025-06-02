# 🎧 Spotify Character Generator

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
git clone https://github.com/yourusername/spotify-character-generator.git
cd spotify-character-generator


### 3. Create a .env file
Make a file called .env in the root directory with the following:

env
Copy
Edit
FLASK_SECRET_KEY=your-secret-key
SPOTIPY_CLIENT_ID=your-spotify-client-id
SPOTIPY_CLIENT_SECRET=your-spotify-client-secret
SPOTIPY_REDIRECT_URI=http://localhost:5000/callback
HUGGINGFACE_TOKEN=your-huggingface-token
SECURITY_TOKEN=your-shared-token
IMAGE_API_URL=https://your-ngrok-tunnel-url.ngrok.io
