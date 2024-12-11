import os
import requests
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()
def get_access_token():
    token_url = os.getenv('OIDC_PROVIDER_TOKEN_URL')
    client_id = os.getenv('SERVICE_ACCOUNT_ID')
    client_secret = os.getenv('SERVICE_ACCOUNT_SECRET') 
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    if not all([token_url, client_id, username, password]):
        raise ValueError("Missing required environment variables.")
    data = {
        'grant_type': 'password',
        'client_id': client_id,
        'username': username,
        'password': password
    }
    if client_secret:
        data['client_secret'] = client_secret
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    token_response = requests.post(token_url, data=data, headers=headers)
    if token_response.status_code != 200:
        raise Exception(f"Failed to get token: {token_response.status_code} - {token_response.text}")
    access_token = token_response.json().get('access_token')
    print(access_token)
    if not access_token:
        raise Exception("Failed to retrieve access token")
    return access_token

def get_users():
    access_token = get_access_token()
    keycloak_server_url = os.getenv('KEYCLOAK_SERVER_URL')
    realm_name = os.getenv('REALM_NAME') 
    
    count_endpoint = f"{keycloak_server_url}/admin/realms/{realm_name}/users/count"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    count_response = requests.get(count_endpoint, headers=headers)
    count_response.raise_for_status()
    total_users = count_response.json()  

    all_users = []
    first = 0
    max_results = 100  

    print("Total Results Found :", total_users)
    while first < total_users:
        users_endpoint = f"{keycloak_server_url}/admin/realms/{realm_name}/users?first={first}&max={max_results}"
        response = requests.get(users_endpoint, headers=headers)
        response.raise_for_status()
        users_data = response.json()

        for user in users_data:
            user_id = user['id']
            print("Processing ", user_id)
            user_groups_endpoint = f"{keycloak_server_url}/admin/realms/{realm_name}/users/{user_id}/groups"
            user_groups_response = requests.get(user_groups_endpoint, headers=headers)
            user_groups_response.raise_for_status()
            
            user_groups = user_groups_response.json()
            
            group_names = [group['name'] for group in user_groups]
            
            user['group_names'] = group_names

        all_users.extend(users_data)
        
        first += max_results

    return all_users

def write_to_csv(filtered_users):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_name = f"users_with_groups_{current_datetime}.csv"
    
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Groups', 'Username', 'Display Name', 'User ID', 'User Email', 'Identity Provider'])
        
        for user in filtered_users:
            groups = user.get('group_names', [])
            display_name = f"{user.get('firstName', '')} {user.get('lastName', '')}".strip()  
            
            if not groups:
                writer.writerow(['N/A',
                                 user.get('username', 'N/A'),
                                 display_name,
                                 user.get('id', 'N/A'),
                                 user.get('email', 'N/A'),
                                 user.get('attributes', {}).get('identity_provider', ['N/A'])[0]])
            else:
                for group in groups:
                    writer.writerow([group,
                                     user.get('username', 'N/A'),
                                     display_name,
                                     user.get('id', 'N/A'),
                                     user.get('email', 'N/A'),
                                     user.get('attributes', {}).get('identity_provider', ['N/A'])[0]])

    print(f"New file created: {csv_file_name}")



if __name__ == "__main__":
    try:
        users_data = get_users()
        count = 0
        filtered_users = []
        for user in users_data:
            attributes = user.get('attributes', {})
            identity_provider = attributes.get('identity_provider', [])
            username = user.get('username', '')
            if 'idir' in identity_provider or '@idir' in username:
                count+=1
                filtered_users.append(user)
            print(count,"total users")

        write_to_csv(filtered_users)
    except Exception as e:
        print(f"Error: {e}")
