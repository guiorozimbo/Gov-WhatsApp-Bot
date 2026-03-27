# Bot WhatsApp para Notificações de Reuniões

Este projeto é um bot automatizado em Python para envio de mensagens WhatsApp relacionadas a reuniões em câmaras municipais brasileiras. Foi desenvolvido e utilizado em uma empresa de governo para acompanhar sessões legislativas, utilizando APIs de estados e cidades do Brasil para filtrar contatos e reuniões.

## Funcionalidades

- **Envio de mensagens de follow-up**: Após reuniões do dia anterior, o bot envia mensagens automáticas para contatos das cidades envolvidas, solicitando feedback e reforçando a importância de enviar ofícios ao Executivo.
- **Integração com Chatwoot**: Busca contatos de usuários registrados na plataforma Chatwoot, associando-os a cidades específicas.
- **Filtragem por datas**: Processa reuniões baseadas em datas (hoje e ontem) a partir de um arquivo JSON de reuniões.
- **Automação via PyWhatKit**: Utiliza a biblioteca PyWhatKit para enviar mensagens instantâneas no WhatsApp, com controle de tempo e fechamento de abas.

## Estrutura do Projeto

- `hoje/`: Scripts para processamento de reuniões do dia atual (se aplicável).
- `todos/`: Scripts para processamento geral ou de todos os contatos.
- `reunioes.json`: Arquivo JSON contendo dados de reuniões, incluindo datas e câmaras municipais.
- `requirements.txt`: Dependências do projeto.
- `.gitignore`: Arquivo para ignorar arquivos sensíveis (como chaves de API e bancos de dados).

## Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **PyWhatKit**: Para automação de envio de mensagens WhatsApp.
- **Requests**: Para integração com APIs (ex.: Chatwoot).
- **PyAutoGUI**: Para simulação de cliques e pressionamento de teclas durante o envio.
- **Unidecode**: Para normalização de textos (remoção de acentos).
- **APIs**: Integração com APIs de estados e cidades do Brasil (via Chatwoot e dados de reuniões).

## Instalação

1. Clone ou baixe o repositório.
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Certifique-se de ter o WhatsApp Web aberto no navegador para o PyWhatKit funcionar.

## Configuração

- **Arquivo `reunioes.json`**: Deve conter um array de objetos com campos como `data` (formato DD/MM/YYYY) e `camara` (nome da cidade/câmara).
- **Configurações de API**: No código, ajuste as variáveis `base_url`, `account_id` e `token` para a sua instância do Chatwoot. **Nunca commite chaves de API no repositório!** Use variáveis de ambiente ou arquivos locais ignorados pelo `.gitignore`.
- **Números de telefone**: Os contatos são extraídos do Chatwoot e formatados automaticamente.

## Como Usar

1. Atualize o `reunioes.json` com as reuniões atuais.
2. Execute o script principal (ex.: `python hoje/envio_mensagem.py`).
3. O bot irá:
   - Ler as reuniões de ontem.
   - Buscar contatos associados às cidades no Chatwoot.
   - Enviar mensagens personalizadas via WhatsApp.
4. Monitore o console para logs de envio.

**Nota**: O envio real está comentado no código para testes. Descomente as linhas de `kit.sendwhatmsg_instantly` para ativar.

## Contexto de Uso

Este projeto foi criado e utilizado em uma empresa de governo para monitorar e acompanhar reuniões legislativas em municípios brasileiros. Integrava-se com APIs públicas de estados e cidades para validar dados de câmaras e contatos, garantindo notificações eficientes para vereadores e envolvidos. A automação reduzia o trabalho manual e melhorava a comunicação institucional.

## Segurança

- Arquivos sensíveis como `PyWhatKit_DB.txt` (banco de dados do PyWhatKit) e chaves de API estão no `.gitignore`.
- Nunca compartilhe tokens ou credenciais públicas.

## Contribuição

Sinta-se à vontade para contribuir com melhorias, mas mantenha a segurança em mente.

## Licença

Este projeto é para uso interno/educacional. Verifique leis de automação de mensagens no Brasil.
