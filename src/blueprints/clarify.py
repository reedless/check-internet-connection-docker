import os

import boto3
import requests

from flask import Blueprint, jsonify

clarify_bp = Blueprint('clarify', __name__)

@clarify_bp.route("/create-job-pytorch", methods=["POST"])
def create_job_pytorch():
    from multiprocessing import Process
    p = Process(target=clarify_main)
    p.start()
    return jsonify({'message': "OK"}), 200

def clarify_main():
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
