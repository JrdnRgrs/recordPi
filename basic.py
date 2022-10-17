import requests
data = {
    'url': 'https://audd.tech/example.mp3',
    'return': 'apple_music,spotify',
    'api_token': 'test'
}
result = requests.post('https://api.audd.io/', data=data)
print(result.text)