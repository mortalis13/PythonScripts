# Basic usage of Tumblr API
# https://www.tumblr.com/docs/en/api/v2

import requests, json


def run_with_app_key():
  """Sends request using a OAuth Consumer Key from a registered app at https://www.tumblr.com/oauth/apps"""
  consumer_key = '...'
  
  url = f'https://api.tumblr.com/v2/blog/programmerhumour/posts?api_key={consumer_key}&npf=true&offset=0&limit=10'
  response = requests.get(url)
  print(response.status_code)
  
  with open('tumblr_response.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(response.json(), indent=2))


def run_with_token():
  """
  Uses a generic token for API calls
  Can be taken from any REST call on Tumblr website, without login
  (through Developer tools, Network, filter XHR, Authorization request header)
  """
  headers = {
    'Authorization': 'Bearer ...'
  }
  
  url = 'https://api.tumblr.com/v2/blog/programmerhumour/posts?npf=true&offset=0&limit=10'
  response = requests.get(url, headers=headers)
  print(response.status_code)
  
  with open('tumblr_response.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(response.json(), indent=2))


run_with_token()
# run_with_app_key()
