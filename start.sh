#!/bin/bash
# Instala os navegadores do Playwright
python3 -m playwright install

# Executa o seu app
python3 web_scrap_get_FIIs.py
