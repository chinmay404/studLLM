import requests

payload = { 'api_key': 'a4b33ac31b951524fa402df2fbeed551', 'query': 'Software' }
r = requests.get('https://api.scraperapi.com/structured/google/jobs', params=payload)
print(r.text)
