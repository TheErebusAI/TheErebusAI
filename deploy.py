import os
import requests
import json

# Load Cloudflare token
with open('/home/erebus/persistent/cloudflare_token', 'r') as f:
    token = f.read().strip().split('=')[1]

HEADERS = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

BASE_URL = 'https://api.cloudflare.com/client/v4'

def get_zone_id(domain='theerebusai.com'):
    try:
        response = requests.get(
            f'{BASE_URL}/zones',
            headers=HEADERS
        )
        response.raise_for_status()
        print(f"Zones Response: {response.text}")
        zones = response.json()
        for zone in zones.get('result', []):
            if zone['name'] == domain:
                return zone['id']
        return None
    except Exception as e:
        print(f"Error getting zone ID: {e}")
        print(f"Response: {response.text if 'response' in locals() else 'No response'}")
        return None

def setup_pages():
    # Get account ID first
    response = requests.get(f'{BASE_URL}/accounts', headers=HEADERS)
    accounts = response.json()
    
    if not accounts.get('result'):
        print("No accounts found or token doesn't have access")
        return
    
    account_id = accounts['result'][0]['id']
    
    # Create Pages project if it doesn't exist
    project_name = 'theerebusai'
    response = requests.post(
        f'{BASE_URL}/accounts/{account_id}/pages/projects',
        headers=HEADERS,
        json={
            'name': project_name,
            'production_branch': 'main'
        }
    )
    
    if response.status_code == 200:
        print("Pages project created/updated successfully")
    else:
        print(f"Error setting up Pages: {response.text}")

def configure_dns(zone_id):
    # Configure DNS for the Pages project
    response = requests.post(
        f'{BASE_URL}/zones/{zone_id}/dns_records',
        headers=HEADERS,
        json={
            'type': 'CNAME',
            'name': '@',
            'content': 'theerebusai.pages.dev',
            'proxied': True
        }
    )
    
    if response.status_code in [200, 409]:  # 409 means record exists
        print("DNS configured successfully")
    else:
        print(f"Error configuring DNS: {response.text}")

def main():
    print("Setting up Cloudflare deployment...")
    
    # Get zone ID
    zone_id = get_zone_id()
    if not zone_id:
        print("Could not find zone ID for domain")
        return
    
    # Setup Pages project
    setup_pages()
    
    # Configure DNS
    configure_dns(zone_id)
    
    print("Deployment setup complete!")

if __name__ == '__main__':
    main()