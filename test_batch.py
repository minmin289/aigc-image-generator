import requests

url = "http://127.0.0.1:5000/batch_generate"
data = {"prompts": ["a cute cat", "a red shoe", "a futuristic city"]}
response = requests.post(url, json=data)
print(response.json())