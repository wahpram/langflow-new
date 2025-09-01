import requests

url = "https://api.apollo.io/api/v1/mixed_people/organization_top_people"

headers = {
    "accept": "application/json",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "x-api-key": "l-dEV1QNQLoR327y842phA"
}
payload = {
    "organization_id": "57c4ace7a6da9867ee5599e7"  # Google
}

response = requests.post(url, headers=headers, json=payload)

print(response.json())