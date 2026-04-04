import requests
import pywhatkit as kit
import time
import re
import pyautogui
from collections import defaultdict

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# === CONFIGURAÇÕES ===
base_url = os.getenv("CHATWOOT_BASE_URL", "https://chat.gwlegis.com.br")
account_id = os.getenv("CHATWOOT_ACCOUNT_ID", "2")
token = os.getenv("CHATWOOT_TOKEN")

if not token:
    print("ERRO: Token do Chatwoot não configurado no arquivo .env")
    exit(1)

headers = {"api_access_token": token}

# === BUSCA TODOS OS CONTATOS COM 'CM' NO NOME ===
page = 1
contatos_cm = []

while True:
    url = f"{base_url}/api/v1/accounts/{account_id}/contacts?page={page}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro na página {page}: {response.status_code}")
        break

    contatos = response.json().get('payload', [])
    if not contatos:
        break

    for contato in contatos:
        nome = contato.get('name', '').strip()
        numero = contato.get('phone_number', '').strip()
        if nome and numero and "CM" in nome:
            numero = re.sub(r'\D', '', numero)
            if len(numero) >= 12:
                partes = nome.split("CM", 1)
                cidade = partes[1].strip() if len(partes) > 1 else "Desconhecida"
                contatos_cm.append({
                    "nome": nome,
                    "numero": f"+{numero}",
                    "cidade": cidade
                })

    page += 1

if not contatos_cm:
    print("Nenhum contato com 'CM' encontrado.")
    exit()

# Caminho da imagem a ser enviada
imagem_path = "imagem.jpg"

# === ENVIO DAS IMAGENS ===
for contato in contatos_cm:
    nome_usuario = contato.get("nome", "Olá").strip()
    numero = contato["numero"]
    cidade = contato.get("cidade", "Desconhecida")

    # Envia a imagem para o número (sem texto adicional)
    kit.sendwhats_image(receiver=numero, img_path=imagem_path, caption="", wait_time=10, tab_close=True)
    time.sleep(10)
    pyautogui.press("enter")
    time.sleep(5)

    print(f"Imagem enviada para {nome_usuario} - ({numero}) - [{cidade}]")

print(f"\nImagens enviadas para {len(contatos_cm)} contatos com 'CM' no nome.")
