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

## 🛠️ Setup
Create a .env file in the root directory:
