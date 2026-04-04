import requests
import json
import os
import re
from datetime import datetime
from collections import defaultdict

from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do Chatwoot
base_url = os.getenv("CHATWOOT_BASE_URL", "https://chat.gwlegis.com.br")
account_id = os.getenv("CHATWOOT_ACCOUNT_ID", "2")
token = os.getenv("CHATWOOT_TOKEN")

if not token:
    print("ERRO: Token do Chatwoot não configurado no arquivo .env")
    exit(1)

headers = { "api_access_token": token }

# Função para buscar as Câmaras do Chatwoot
def obter_camaras():
    page = 1
    cidades = set()

    while True:
        url = f"{base_url}/api/v1/accounts/{account_id}/contacts?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Erro na página {page}: {response.status_code}")
            break

        contatos = response.json().get("payload", [])
        if not contatos:
            break

        for contato in contatos:
            nome = contato.get("name", "")
            if "CM" in nome:
                partes = nome.split("CM", 1)
                cidade = partes[1].strip()
                cidades.add(cidade)

        page += 1

    return sorted(cidades)

# Caminho do arquivo JSON
arquivo_json = "reunioes.json"

# Puxa câmaras disponíveis
camaras_disponiveis = obter_camaras()

# Carrega ou cria arquivo JSON
if os.path.exists(arquivo_json):
    with open(arquivo_json, "r", encoding="utf-8") as f:
        reunioes = json.load(f)
else:
    reunioes = []

while True:
    print("\nCâmaras disponíveis:")
    for i, camara in enumerate(camaras_disponiveis, start=1):
        print(f"{i}. {camara}")

    entrada = input("\nDigite os números das câmaras desejadas (separados por vírgula ou 'sair' para encerrar): ").strip()
    if entrada.lower() in ["", "sair"]:
        break

    numeros = [num.strip() for num in entrada.split(",")]

    camaras_selecionadas = []
    for num in numeros:
        try:
            indice = int(num) - 1
            if 0 <= indice < len(camaras_disponiveis):
                camaras_selecionadas.append(camaras_disponiveis[indice])
            else:
                print(f"❌ Número inválido: {num}")
        except ValueError:
            print(f"❌ Valor inválido: {num}")

    if not camaras_selecionadas:
        print("⚠️ Nenhuma câmara válida selecionada.")
        continue

    data_input = input("Quando será a reunião? (formato: DD/MM/AAAA): ").strip()
    try:
        data_formatada = datetime.strptime(data_input, "%d/%m/%Y").strftime("%d/%m/%Y")
    except ValueError:
        print("❌ Formato de data inválido.")
        continue

    novos_registros = 0
    for camara in camaras_selecionadas:
        registro = {"data": data_formatada, "camara": camara}
        if registro not in reunioes:
            reunioes.append(registro)
            novos_registros += 1

    with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump(reunioes, f, ensure_ascii=False, indent=4)

    print(f"\n✅ {novos_registros} reunião(ões) registrada(s) para o dia {data_formatada}.")
    for c in camaras_selecionadas:
        print(f" - {c}")

print("\n📝 Registro de reuniões encerrado.")
