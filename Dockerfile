# ベースイメージとして ollama/ollama を使用
FROM ollama/ollama

# 環境変数を設定
ENV OLLAMA_HOST=http://localhost:11434

# サーバーを起動し、モデルをプルするスクリプトを作成
RUN echo "#!/bin/sh\n\
ollama serve &\n\
sleep 10\n\
ollama pull gemma2:2b" > /usr/local/bin/start_and_pull.sh && \
    chmod +x /usr/local/bin/start_and_pull.sh

# ベースイメージとしてPython 3.9を使用
FROM python:3.9-slim

# システムレベルの依存関係をインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# Pythonパッケージの依存関係ファイルをコピー
COPY Docker_requirements.txt /app/

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r Docker_requirements.txt





# アプリケーションの全ファイルをコンテナにコピー
COPY . /app/

# ポートを公開 (Djangoのデフォルトは8000)
EXPOSE 8000

# 開発用サーバーの起動コマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
