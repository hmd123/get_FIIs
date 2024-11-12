#!/bin/bash

# Atualiza o sistema e instala as dependências necessárias
apt-get update -y
apt-get install -y \
    libgstgl-1.0.so.0 \
    libgstcodecparsers-1.0.so.0 \
    libenchant-2.so.2 \
    libsecret-1.so.0 \
    libmanette-0.2.so.0 \
    libGLESv2.so.2 \
    wget
    
# Instala os navegadores do Playwright
python3 -m playwright install

# Executa o seu app
python3 web_scrap_get_FIIs.py

# Finaliza com o seu script Python
python3 app.py
