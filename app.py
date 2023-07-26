#app.py
import os

import boto3
import requests

import serverless_wsgi
from flask import Flask
from src.blueprints.clarify import clarify_bp

app = Flask(__name__)

app.register_blueprint(clarify_bp, url_prefix='/clarify')

@app.route("/")
def hello_world():
    response = requests.get("https://www.example.com/")
    print(response.text)
    s3 = boto3.client('s3')
    s3.list_objects(Bucket="xai-assets")

    writable_dir = "/tmp/"

    s3.download_file("xai-assets", "noise_rgb.png", os.path.join(writable_dir, "noise_rgb.png"))

    print("Before mkdirs")
    os.makedirs(os.path.join(writable_dir, 'model'), exist_ok=True)
    
    print("Before download")
    bucketName = "sample-xai-clarify-input"
    model_file='model/model.py'
    model_weights='model/model.pt'
    s3.download_file(bucketName, model_file, os.path.join(writable_dir, 'model', 'model.py'))
    s3.download_file(bucketName, model_weights, os.path.join(writable_dir, 'model', 'model.pt'))
    print("Download success")

    return response.text

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
