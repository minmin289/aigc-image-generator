from http.client import responses

import requests
import json
import base64
from PIL import Image
from io import BytesIO

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
payload = {
    "prompt": "a cute cat, high resolution",
    "negative_prompt": "ugly",
    "steps": 20,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "sampler_index": "Euler a"
}
response = requests.post(url, json=payload)
r = response.json()
image_data = base64.b64decode(r["images"][0])
image = Image.open(BytesIO(image_data))
image.save("cat.png")
print("图片已保存为cat.png")