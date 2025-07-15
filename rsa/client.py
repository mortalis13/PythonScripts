import requests
response = requests.get('https://127.0.0.1:5000/items', cert=('client.crt', 'client.key'), verify='ca.crt')

print(response.status_code)
print(response.text)
