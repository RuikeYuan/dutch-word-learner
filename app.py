from flask import Flask, render_template, jsonify, request, send_file
import dutch_words
import torch
from diffusers import FluxPipeline
from io import BytesIO

app = Flask(__name__)

# Get the list of ranked Dutch words
ranked_words = dutch_words.get_ranked()

# Total number of words
total_words = len(ranked_words)

# Number of words per level (10% of the total)
words_per_level = total_words // 10

# Create the levels and the words_data list
levels = {}
words_data = []  # List to hold all words with their levels

for i in range(10):
    level_start = i * words_per_level
    level_end = (i + 1) * words_per_level if i < 9 else total_words
    level_number = i + 1
    levels[level_number] = ranked_words[level_start:level_end]

    # Add words to the words_data list with their respective level
    for word in ranked_words[level_start:level_end]:
        words_data.append({"word": word, "rank": level_number})

# Initialize an empty review list
review_list = []

# Initialize the image generation model
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload()

@app.route('/')
def index():
    return render_template('index.html', words_data=words_data)

@app.route('/words')
def get_words():
    return jsonify(words_data)

@app.route('/add-to-review', methods=['POST'])
def add_to_review():
    data = request.json
    word = data.get('word')

    if word and word not in review_list:
        review_list.append(word)

    return jsonify({'status': 'success'})

@app.route('/review')
def get_review():
    return jsonify(review_list)

@app.route('/review-list')
def review_list_page():
    return render_template('review_list.html', review_list=review_list)

@app.route('/generate_image/<word>')
def generate_image(word):
    prompt = f"A cat holding a sign that says {word}"

    # Generate image based on the prompt
    image = pipe(
        prompt,
        height=1024,
        width=1024,
        guidance_scale=3.5,
        num_inference_steps=50,
        max_sequence_length=512,
        generator=torch.Generator("cpu").manual_seed(0)
    ).images[0]

    # Save image to a BytesIO object
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    # Send the image file
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
