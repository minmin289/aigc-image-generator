from PIL.SpiderImagePlugin import isInt
from flask import Flask, request, send_file, jsonify
from jinja2.sandbox import is_internal_attribute

from sd_engine import generate_image
import uuid
import os

app = Flask(__name__)

OUTPUT_DIR = "generated_iamges"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.route('/generate')
def generate():
    prompt = request.args.get('prompt', '')

    if not prompt:
        return "错误：缺少 prompt 参数", 400

    image = generate_image(prompt)
    if image is None:
        return "生成图片失败，请检查 SD WebUI 是否运行", 500

    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    image.save(filepath)

    return send_file(filepath, mimetype='image/png')


@app.route('/batch_generate', methods=['POST'])
def batch_generate():
    data = request.get_json()
    if not data or 'prompts' not in data:
        return jsonify({"error": "请提供prompts列表"}), 400
    prompts = data['prompts']
    if not isinstance(prompts, list):
        return jsonify({"error": "prompts必须是一个列表"}), 400

    results = []

    for idx, prompt in enumerate(prompts):
        image = generate_image(prompt)
        if image is None:
            results.append({"prompt": prompt, "status": "failed", "image_url": None})
            continue

        filename = f"{uuid.uuid4().hex}.png"
        filepath =os.path.join(OUTPUT_DIR,filename)
        image.save(filepath)

        image_url =f"http://127.0.0.1:5000/images/{filename}"
        results.append({"prompt": prompt, "status": "success", "image_url": image_url})

    return jsonify({"results":results})

@app.route('/images/<filename>')
def get_image(filename):
    return send_file(os.path.join(OUTPUT_DIR, filename), mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
