from fastapi import FastAPI
import requests

import tensorflow as tf
from transformers import AutoTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

url = 's3://psyclepub/bert-base-multilingual-uncased.tflite'
filename = 'bert-base-multilingual-uncased.tflite'

response = requests.get(url)
with open(filename, 'wb') as f:
    f.write(response.content)

tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-uncased")
interpreter = tf.lite.Interpreter(model_path="bert-base-multilingual-uncased.tflite")

interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

sentiment = ["Positive | Happy", "Surprised | Confused", "Negative | Sad", "Negative | Angry"]

bertAPI = FastAPI()
@bertAPI.post("/getSentiment")
async def req(data: str):
    input_data = pad_sequences([tokenizer.encode(data, max_length = 32, padding = "max_length", truncation = True)], maxlen=32, truncating = "post", padding = "post")
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return f"{sentiment[np.argmax(output_data[0])]}"
