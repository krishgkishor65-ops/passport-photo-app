from flask import Flask, render_template, request
from PIL import Image, ImageEnhance
from rembg import remove
import io
import base64
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def auto_center_face(pil_img):
    img = np.array(pil_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return pil_img

    (x, y, w, h) = faces[0]

    padding_top = int(h * 0.6)
    padding_side = int(w * 0.5)
    padding_bottom = int(h * 0.8)

    x1 = max(0, x - padding_side)
    y1 = max(0, y - padding_top)
    x2 = min(img.shape[1], x + w + padding_side)
    y2 = min(img.shape[0], y + h + padding_bottom)

    cropped = img[y1:y2, x1:x2]
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)

    return Image.fromarray(cropped)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    bgcolor = request.form['bgcolor']
    brightness_value = float(request.form['brightness'])
    copies = int(request.form['copies'])

    img = Image.open(file)

    # Face center
    img = auto_center_face(img)

    # Remove background
    img = remove(img)

    colors = {
        "white": (255, 255, 255),
        "blue": (0, 102, 255),
        "red": (255, 0, 0),
        "green": (0, 200, 0),
        "yellow": (255, 255, 0),
        "pink": (255, 105, 180),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "black": (0, 0, 0),
        "gray": (128, 128, 128),
        "skyblue": (135, 206, 235),
        "cream": (255, 253, 208)
    }

    color = colors.get(bgcolor, (255, 255, 255))

    bg = Image.new("RGB", img.size, color)
    bg.paste(img, mask=img.split()[3])

    # Enhance
    bg = ImageEnhance.Sharpness(bg).enhance(2.0)
    bg = ImageEnhance.Contrast(bg).enhance(1.5)
    bg = ImageEnhance.Brightness(bg).enhance(brightness_value)

    # Resize passport
    bg = bg.resize((413, 531))

    # Grid
    width, height = bg.size
    border = 10
    cols = 2
    rows = copies // 2

    grid_width = cols * width + (cols + 1) * border
    grid_height = rows * height + (rows + 1) * border

    grid = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

    for i in range(copies):
        col = i % cols
        row = i // cols

        x = col * width + (col + 1) * border
        y = row * height + (row + 1) * border

        grid.paste(bg, (x, y))

    img_io = io.BytesIO()
    grid.save(img_io, 'JPEG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template("result.html", image_data=img_base64)

if __name__ == "__main__":
    app.run()from flask import Flask, render_template, request
from PIL import Image, ImageEnhance
from rembg import remove
import io
import base64
import cv2
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def auto_center_face(pil_img):
    img = np.array(pil_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return pil_img

    (x, y, w, h) = faces[0]

    padding_top = int(h * 0.6)
    padding_side = int(w * 0.5)
    padding_bottom = int(h * 0.8)

    x1 = max(0, x - padding_side)
    y1 = max(0, y - padding_top)
    x2 = min(img.shape[1], x + w + padding_side)
    y2 = min(img.shape[0], y + h + padding_bottom)

    cropped = img[y1:y2, x1:x2]
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)

    return Image.fromarray(cropped)

@app.route('/process', methods=['POST'])
def process():
    file = request.files['image']
    bgcolor = request.form['bgcolor']
    brightness_value = float(request.form['brightness'])
    copies = int(request.form['copies'])

    img = Image.open(file)

    # Face center
    img = auto_center_face(img)

    # Remove background
    img = remove(img)

    colors = {
        "white": (255, 255, 255),
        "blue": (0, 102, 255),
        "red": (255, 0, 0),
        "green": (0, 200, 0),
        "yellow": (255, 255, 0),
        "pink": (255, 105, 180),
        "orange": (255, 165, 0),
        "purple": (128, 0, 128),
        "black": (0, 0, 0),
        "gray": (128, 128, 128),
        "skyblue": (135, 206, 235),
        "cream": (255, 253, 208)
    }

    color = colors.get(bgcolor, (255, 255, 255))

    bg = Image.new("RGB", img.size, color)
    bg.paste(img, mask=img.split()[3])

    # Enhance
    bg = ImageEnhance.Sharpness(bg).enhance(2.0)
    bg = ImageEnhance.Contrast(bg).enhance(1.5)
    bg = ImageEnhance.Brightness(bg).enhance(brightness_value)

    # Resize passport
    bg = bg.resize((413, 531))

    # Grid
    width, height = bg.size
    border = 10
    cols = 2
    rows = copies // 2

    grid_width = cols * width + (cols + 1) * border
    grid_height = rows * height + (rows + 1) * border

    grid = Image.new("RGB", (grid_width, grid_height), (255, 255, 255))

    for i in range(copies):
        col = i % cols
        row = i // cols

        x = col * width + (col + 1) * border
        y = row * height + (row + 1) * border

        grid.paste(bg, (x, y))

    img_io = io.BytesIO()
    grid.save(img_io, 'JPEG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

    return render_template("result.html", image_data=img_base64)

if __name__ == "__main__":
    app.run()