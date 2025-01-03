import requests, base64


def set_checkpoint(model_name):
    # options エンドポイントを使ってチェックポイントを設定
    options_payload = {
        "sd_model_checkpoint": model_name
    }
    response = requests.post('http://127.0.0.1:7860/sdapi/v1/options', json=options_payload)
    if response.status_code == 200:
        print(f"Checkpoint set to {model_name}")
    else:
        print("Failed to set checkpoint")

def generate_image():
    # 画像生成設定
    Imgsetting = {
        "prompt": "(masterpiece, exquitive, photorealistic, best quality:1.1), 1girl, japanese, solo",
        "negative_prompt": "(worst quality, bad quality, low quality:1.2),nsfw",
        "steps": 20,
        "sampler_index": "DPM++ 2M Karras",
        "width": 512,
        "height": 640,
        "cfg_scale": 7,
        "seed": -1,
    }

    # 画像生成リクエストを送信
    resp = requests.post(url=f'http://127.0.0.1:7860/sdapi/v1/txt2img', json=Imgsetting)
    json_resp = resp.json()

    # 画像をデコードして保存
    imgdata = json_resp["images"][0]
    with open("test1.png", "wb") as f:
        buf = base64.b64decode(imgdata)
        f.write(buf)
    print("Image generated and saved as test1.png")

def main():
    # チェックポイントを指定
    cp_yayoi = "3D\yayoiMix_v20.safetensors"
    set_checkpoint(cp_yayoi)  # まずチェックポイントを設定
    generate_image()           # 次に画像生成をリクエスト

if __name__ == '__main__':
    main()
