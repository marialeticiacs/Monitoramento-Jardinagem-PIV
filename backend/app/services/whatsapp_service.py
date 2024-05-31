import requests

def enviar_mensagem_whatsapp(telefone, api_key, mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?phone={telefone}&text={mensagem}&apikey={api_key}"
    response = requests.get(url)
    return response.status_code
