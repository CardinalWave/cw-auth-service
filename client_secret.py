import time
import requests

def capture_client_secret():
    keycloak_url = "http://localhost:8080"

    data = {
        'username': 'admin',
        'password': 'admin',
        'grant_type': 'password',
        'client_id': 'admin-cli'
    }

    response = requests.post(f"{keycloak_url}/realms/master/protocol/openid-connect/token", data=data)
    if response.status_code != 200:
        print(f"Erro ao obter token de acesso: {response.text}")
        exit()

    access_token = response.json().get('access_token')
    if not access_token:
        print("Token de acesso não encontrado na resposta")
        exit()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    clients_response = requests.get(f"{keycloak_url}/admin/realms/master/clients", headers=headers)
    if clients_response.status_code != 200:
        print(f"Erro ao buscar clientes: {clients_response.text}")
        exit()

    clients = clients_response.json()
    client_id = None
    for client in clients:
        if client.get('clientId') == 'master-realm':
            client_id = client.get('id')
            print(client)
            break

    if not client_id:
        print("PythonClient não encontrado")
        exit()

    secret_response = requests.get(f"{keycloak_url}/admin/realms/master/clients/{client_id}/client-secret", headers=headers)
    if secret_response.status_code != 200:
        print(f"Erro ao obter o segredo do cliente: {secret_response.text}")
        exit()
    print(secret_response.text)
    client_secret = secret_response.json().get('value')
    if not client_secret:
        print("Segredo do cliente não encontrado")
        exit()

    with open('/opt/keycloak/data/client_secret.env', 'w') as file:
        file.write(f"CLIENT_SECRET={client_secret}\n")

    print("Segredo do cliente salvo com sucesso!")

capture_client_secret()