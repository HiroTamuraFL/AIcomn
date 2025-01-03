import requests
from django.conf import settings

# Ollama APIのエンドポイント
OLLAMA_URL = settings.OLLAMA_API_URL  # docker-compose内で 'ollama' がホスト名になります

def get_data_from_ollama(payload):
    """
    Ollama APIにデータを送信し、レスポンスを取得する関数
    """
    url = f"{OLLAMA_URL}/your_endpoint"  # 置き換え: Ollamaのエンドポイント
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()  # 必要に応じてレスポンスを処理
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama API: {e}")
        return None
