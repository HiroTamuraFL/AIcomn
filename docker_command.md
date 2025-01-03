不要なイメージの削除
docker system prune -a


redis サーバの起動
docker-compose up -d redis



wsl --list --verbose

Ubuntuの起動
wsl --install Ubuntu
wsl --install -d Ubuntu-22.04


ドライブの移動
cd /mnt/f

VSCodeを起動
code .


SDの起動
cd stable-diffusion-webui-docker
docker compose --profile auto up --build

不要なキャッシュの削除
docker system prune -a

* 実行コマンド
    - docker-compose up -d stable-diffusion
    - docker-compose up -d ollama
    - docker-compose exec ollama ollama pull gemma2:2b
    - docker-compose up -d


* Ubuntuの仮想ドライブが大きくなりすぎたとき(再セットアップ)
    1. wsl --shutdown
    2. wsl --unregister Ubuntu
    3. 仮想ドライブを消す
    4. (base) PS C:\Users\81901> wsl --import Ubuntu G:\WSL\Ubuntu G:\WSL\Ubuntu\ubuntu_backup_v2.tar 

        5. docker-compose の導入 https://chatgpt.com/c/ 671ec334-c4d8-8012-8cfc-5dc4af584c6e 
    6. ollamaにLLMをpull
        docker-compose up -d ollama
        docker-compose exec ollama ollama pull gemma2:2b

    7. nvidia driverのインストール
    https://soroban.highreso.jp/article/article-091 
        1. distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
        1. ドライバーをリセット
            $sudo rm /etc/apt/sources.list.d/nvidia-container-toolkit.list
            $sudo rm /etc/apt/sources.list.d/nvidia-docker.list
        2. sudo nano /etc/apt/sources.list.d/nvidia-container-toolkit.listを実行して中身を以下にする
            #deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu22.04/amd64 /
            deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/nvidia-container-runtime/stable/ubuntu22.04/amd64 /
            deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/nvidia-docker/ubuntu22.04/amd64 /
        3. sudo apt update
        4. distribution=$(. /etc/os-release; echo $ID$VERSION_ID)
        5. curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
        6. curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list |   sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' |   sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
        7. sudo apt update
        8. sudo apt install -y nvidia-container-toolkit
        9. sudo nvidia-ctk runtime configure --runtime=docker
        10. sudo service docker restart