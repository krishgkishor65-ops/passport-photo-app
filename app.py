from flask import Flask, render_template, request
from PIL import Image, ImageEnhance
import io
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    bgcolor = request.form['bgcolor']
    brightness_value = float(request.form['brightness'])

    img = Image.open(file).convert("RGB")

    # Background colors
    colors = {
        "white": (255, 255, 255),
        "blue": (0, 102, 255),
        "red": (255, 0, 0),
        "green": (0, 200, 0)
    }

    color = colors.get(bgcolor, (255, 255, 255))
    bg = Image.new("RGB", img.size, color)
    bg.paste(img)

    # Brightness
    bg = ImageEnhance.Brightness(bg).enhance(brightness_value)

    # Resize passport size
    bg = bg.resize((413, 531))

    # Convert to base64
    img_io = io.BytesIO()
    bg.save(img_io, 'JPEG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template("result.html", image_data=img_base64)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
