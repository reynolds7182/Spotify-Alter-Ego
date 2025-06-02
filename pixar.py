import os
import base64
import subprocess
from flask import Flask, request, redirect, session, url_for, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
import re
import torch
from diffusers import StableDiffusionPipeline  # Make sure this is at the top
import uuid
from flask import render_template
from dotenv import load_dotenv
load_dotenv()


from huggingface_hub import login
login(os.getenv("HUGGINGFACE_TOKEN"))

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = 'user-top-read user-read-recently-played'

login(os.getenv("HUGGINGFACE_TOKEN"))

# Initialize globals
sp = None
sp_oauth = None
cache_handler = None

# Load Stable Diffusion + LoRA model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")


from diffusers import StableDiffusionPipeline  

pipe = StableDiffusionPipeline.from_pretrained(
    "Lykon/dreamshaper-8",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)

pipe.to(device)
pipe.enable_attention_slicing()
if device == "cuda":
    pipe.enable_model_cpu_offload()
elif device == "mps":
    pipe.enable_vae_slicing()


@app.before_request
def before_request():
    global sp, sp_oauth, cache_handler
    cache_handler = FlaskSessionCacheHandler(session)
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=SCOPE,
        cache_handler=cache_handler,
        show_dialog=False
    )
    token_info = cache_handler.get_cached_token()
    if token_info:
        sp = Spotify(auth=token_info['access_token'])
    else:
        sp = None

@app.route('/')
def home():
    if not sp:
        return redirect(sp_oauth.get_authorize_url())
    try:
        top_tracks_data = get_top_tracks_data()
        recent_tracks_data = get_recent_tracks_data()
        return jsonify({
            'status': 'success',
            'top_tracks': top_tracks_data,
            'recent_tracks': recent_tracks_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ui')
def ui():
    return render_template('index.html')

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    token_info = sp_oauth.get_access_token(code, as_dict=True)
    if not token_info:
        return jsonify({'error': 'Could not get token'}), 400
    return redirect(url_for('home'))

def get_top_tracks_data():
    if not sp:
        raise Exception("Spotify client not initialized")
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='long_term')
    tracks_data = []
    for track in top_tracks['items']:
        track_info = {
            'id': track['id'],
            'name': track['name'],
            'artists': [artist['name'] for artist in track['artists']],
            'album': track['album']['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'external_urls': track['external_urls']['spotify'],
            'preview_url': track['preview_url']
        }
        if track['album']['images']:
            track_info['album_cover'] = track['album']['images'][0]['url']
        tracks_data.append(track_info)
    return tracks_data

def get_recent_tracks_data():
    if not sp:
        raise Exception("Spotify client not initialized")
    recent_tracks = sp.current_user_recently_played(limit=50)
    seen_tracks = set()
    unique_tracks = []
    for item in recent_tracks['items']:
        track = item['track']
        track_id = track['id']
        if track_id not in seen_tracks:
            seen_tracks.add(track_id)
            track_info = {
                'id': track['id'],
                'name': track['name'],
                'artists': [artist['name'] for artist in track['artists']],
                'album': track['album']['name'],
                'popularity': track['popularity'],
                'duration_ms': track['duration_ms'],
                'external_urls': track['external_urls']['spotify'],
                'preview_url': track['preview_url'],
                'played_at': item['played_at']
            }
            if track['album']['images']:
                track_info['album_cover'] = track['album']['images'][0]['url']
            unique_tracks.append(track_info)
            if len(unique_tracks) >= 10:
                break
    return unique_tracks

def call_ollama(prompt):
    """Call Ollama CLI to get a generated character description from the prompt."""
    model_name = "llama3"
    result = subprocess.run(
        ["ollama", "run", model_name],
        input=prompt,
        text=True,
        capture_output=True
    )
    if result.returncode != 0:
        raise Exception(f"Error calling Ollama: {result.stderr}")
    return result.stdout.strip()


def parse_ollama_response(response):
    import re
    description = ""
    image_prompt = ""

    desc_match = re.search(r"### DESCRIPTION\s*(.+?)\s*### IMAGE", response, re.DOTALL | re.IGNORECASE)
    image_match = re.search(r"### IMAGE\s*(.+)", response, re.DOTALL | re.IGNORECASE)

    if desc_match:
        description = desc_match.group(1).strip()
    if image_match:
        image_prompt = image_match.group(1).strip()

    return description, image_prompt


def build_prompt(top_tracks, recent_tracks):
    with open("pixar_prompt.txt", "r") as f:
        template = f.read()

    top_str = '\n'.join(f"- '{t['name']}' by {', '.join(t['artists'])}" for t in top_tracks)
    recent_str = '\n'.join(f"- '{t['name']}' by {', '.join(t['artists'])}" for t in recent_tracks)

    prompt = template.replace("{{TOP_TRACKS}}", top_str)
    prompt = prompt.replace("{{RECENT_TRACKS}}", recent_str)

    return prompt


def format_image_prompt(image_prompt):
    return (
        "Pixar-style 3D character portrait. Bust shot, centered face, expressive cartoon features, big eyes, cinematic lighting. " +
        image_prompt
    )


def generate_character_image(prompt, output_dir="static"):
    """Generate a Pixar-style cartoon image from the prompt using Stable Diffusion with LoRA."""
    image = pipe(prompt, guidance_scale=7.5, num_inference_steps=30).images[0]

    os.makedirs(output_dir, exist_ok=True)
    filename = f"{uuid.uuid4()}.png"
    output_path = os.path.join(output_dir, filename)
    image.save(output_path)

    return output_path


@app.route('/character')
def character():
    if not sp:
        return redirect(sp_oauth.get_authorize_url())

    try:
        top_tracks = get_top_tracks_data()
        recent_tracks = get_recent_tracks_data()

        ollama_prompt = build_prompt(top_tracks, recent_tracks)
        ollama_response = call_ollama(ollama_prompt)
        character_description, image_prompt = parse_ollama_response(ollama_response)

        # 💡 Apply consistent visual style here
        formatted_prompt = format_image_prompt(image_prompt)
        image_path = generate_character_image(formatted_prompt)

        return jsonify({
            "ollama_prompt": ollama_prompt,
            "character_description": character_description,
            "image_prompt": image_prompt,
            "formatted_prompt": formatted_prompt,
            "image_url": url_for('static', filename=os.path.basename(image_path))
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/recent-tracks')
def recent_tracks_only():
    if not sp:
        return redirect(sp_oauth.get_authorize_url())

    try:
        data = get_recent_tracks_data()
        return jsonify({'recent_tracks': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/user-info')
def user_info():
    if not sp:
        return redirect(sp_oauth.get_authorize_url())

    try:
        user = sp.current_user()
        user_data = {
            'id': user['id'],
            'display_name': user['display_name'],
            'email': user.get('email'),
            'followers': user['followers']['total'],
            'country': user.get('country'),
            'product': user.get('product'),
        }
        if user.get('images'):
            user_data['profile_image'] = user['images'][0]['url']
        return jsonify({'user': user_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
