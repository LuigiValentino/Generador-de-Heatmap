from flask import Flask, request, render_template, Response, jsonify, send_from_directory
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No se subió ningún archivo'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ninguna imagen'}), 400
    
    img = Image.open(file).convert('L')  
    img_array = np.array(img)

    figsize = (img.width / 100, img.height / 100) 

    plt.figure(figsize=figsize)
    sns.heatmap(img_array, cmap='plasma', cbar=True, xticklabels=False, yticklabels=False)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    heatmap_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return jsonify({'heatmap': heatmap_base64})

if __name__ == '__main__':
    app.run(debug=True)
