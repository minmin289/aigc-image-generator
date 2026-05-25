# sd_engine.py
import requests
import base64
import time
from PIL import Image
from io import BytesIO

SD_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

DEFAULT_PAYLOAD = {
    "negative_prompt": "ugly, blurry, low quality",
    "steps": 20,
    "cfg_scale": 7,
    "width": 512,
    "height": 512,
    "sampler_index": "Euler a"
}

def generate_image(prompt, retries=2):
    payload = DEFAULT_PAYLOAD.copy()
    payload["prompt"] = prompt
    for attempt in range(retries):
        try:
            response = requests.post(SD_URL, json=payload, timeout=60)
            if response.status_code == 200:
                r = response.json()
                if "images" in r and len(r["images"]) > 0:
                    image_data = base64.b64decode(r["images"][0])
                    image = Image.open(BytesIO(image_data))
                    return image
        except Exception as e:
            print(f"异常: {e}, 重试 {attempt+1}/{retries}")
        time.sleep(2)
    return None