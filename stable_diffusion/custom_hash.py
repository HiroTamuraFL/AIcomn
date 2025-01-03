import hashlib
import os

def calculate_hash(filepath):
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def hash_checkpoints():
    checkpoint_dir = "./stable-diffusion-webui-docker/data/models/Stable-diffusion"
    files = [
        "./stable-diffusion-webui-docker/data/models/Stable-diffusion/yden_v30.safetensors",
        "./stable-diffusion-webui-docker/data/models/Stable-diffusion/SDXL/hadukiMix_v15.safetensors"
        ]
    for file in files:
        if file.endswith(".ckpt") or file.endswith(".safetensors"):
            #filepath = os.path.join(checkpoint_dir, file)
            filepath = file
            file_hash = calculate_hash(filepath)
            print(f"File: {file}, Hash: {file_hash}")

if __name__ == "__main__":
    hash_checkpoints()
