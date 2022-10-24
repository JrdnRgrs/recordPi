import requests

url = "https://api-v2.acrcloud.com/api/fs-containers/:12209/files?page=1&per_page=20"

payload={}
headers = {
  'Accept': 'application/json',
  'Authorization': 'Bearer token'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)