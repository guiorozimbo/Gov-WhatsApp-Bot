import requests
import pywhatkit as kit
import time
import re
import pyautogui
import json
from datetime import datetime, timedelta
from collections import defaultdict
from unidecode import unidecode

# === CONFIGURAÇÕES ===
base_url = "https://chat.gwlegis.com.br"
account_id = 2
token = "qdC8V1HGXHKruy4wWj4XsydC"
headers = {"api_access_token": token}

# === OBTÉM DATAS ===
hoje = datetime.now()
ontem = hoje - timedelta(days=1)
data_hoje = hoje.strftime("%d/%m/%Y")
data_ontem = ontem.strftime("%d/%m/%Y")

# === LÊ JSON DE REUNIÕES ===
with open("reunioes.json", "r", encoding="utf-8") as f:
    reunioes = json.load(f)

# Cidades com reunião hoje e ontem
cidades_hoje = [item["camara"] for item in reunioes if item["data"] == data_hoje]
cidades_ontem = [item["camara"] for item in reunioes if item["data"] == data_ontem]

if not cidades_hoje and not cidades_ontem:
    print(f"Nenhuma reunião marcada para hoje ({data_hoje}) ou ontem ({data_ontem}).")
    exit()

# === BUSCA CONTATOS NO CHATWOOT ===
page = 1
contatos_por_cidade = defaultdict(list)

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
        if nome and numero:
            numero = re.sub(r'\D', '', numero)
            if len(numero) >= 12:
                cidade = "Desconhecida"
                if "CM" in nome:
                    partes = nome.split("CM", 1)
                    cidade = partes[1].strip()
                contatos_por_cidade[cidade].append({
                    "nome": nome,
                    "numero": f"+{numero}",
                    "cidade": cidade
                })

    page += 1

# === SELECIONA CONTATOS DE CIDADES COM REUNIÃO ONTEM ===
contatos_selecionados = []

for cidade in cidades_ontem:
    contatos = contatos_por_cidade.get(cidade, [])
    for contato in contatos:
        contato["cidade"] = cidade
        contatos_selecionados.append(contato)

if not contatos_selecionados:
    print(f"Nenhum contato encontrado para as cidades com reunião ontem: {', '.join(cidades_ontem)}")
    exit()

# === ENVIA MENSAGENS PARA OS CONTATOS DAS CIDADES ONTEM (APENAS PRINT) ===
for contato in contatos_selecionados:
    cidade = contato.get("cidade", "")
    nome_usuario = contato.get("nome", "Olá").strip()

    mensagem = (
        f"Bom dia, {nome_usuario}! Passando para saber como foi a sessão de ontem. "
        "Se tiver algum feedback, adoraríamos saber! Aproveito para reforçar a importância do envio do ofício ao Executivo. "
        "Caso já tenha feito e recebido essa mensagem, favor desconsiderar esta mensagem. Obrigado! Suporte Governo Web."
    )

    print(f"Para {nome_usuario} ({contato['numero']}), cidade {cidade}:\n{mensagem}\n")

    # Descomente para enviar a mensagem via WhatsApp
    kit.sendwhatmsg_instantly(contato['numero'], mensagem, wait_time=7, tab_close=True)
    time.sleep(10)
    pyautogui.press("enter")
    time.sleep(5)

print(f"\nMensagens preparadas para {len(contatos_selecionados)} contatos das cidades: {', '.join(cidades_ontem)}.")
