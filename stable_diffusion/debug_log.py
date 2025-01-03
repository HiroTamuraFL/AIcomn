import json
import requests
import base64
import cv2

base_url = 'http://stable-diffusion:7860'

# デバッグ情報を保持する辞書
debug_data = {
    "available_models": None,
    "available_modules": None,
    "controlnet_args": None,
    "Imgsetting": None,
    "response_info": None,
    "errors": [],
}

def save_debug_to_json(filepath='debug_output.json'):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(debug_data, f, ensure_ascii=False, indent=4)
    print(f"Debug information saved to {filepath}")

def write_log(**kwargs):
    """
    任意のキーワード引数を受け取り、それをデバッグ辞書に記録する。
    既存のキーが指定された場合は上書きし、新しいキーは追加される。
    """
    for key, value in kwargs.items():
        if key=='error':
            debug_data[key].append(value)
        elif key in debug_data:
            # 既存のキーの場合、内容を上書き
            debug_data[key] = value
        else:
            # 新しいキーの場合、追加
            debug_data[key] = value
    print(f"Log updated with: {kwargs}")