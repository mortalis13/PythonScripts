# Github Copilot REST tester
# Put the token from AppData\Local\github-copilot\apps.json :: oauth_token
# to .copilot_token

import requests
import uuid
import json

MODELS = [
  'gpt-4.1',
  'gpt-4o',
  'gpt-4o-mini',
  
  'gpt-4o-2024-11-20',
  'gpt-4o-2024-08-06',
  'gpt-4o-2024-05-13',
  
  'gpt-4',
  
  'gpt-3.5-turbo',
  
  'o1-preview',
  'o1-mini',
]

def _get_token():
  print('Getting token')
  
  with open('.copilot_token', 'r') as f:
      access_token = f.read()
  
  headers = {
    'authorization': f'token {access_token}',
    'editor-version': 'vscode/1.100.3',
  }
  url = 'https://api.github.com/copilot_internal/v2/token'
  response = requests.get(url, headers=headers)
  token = response.json().get('token')
  
  return token


def get_completions(text: str = None, custom_body: dict = None) -> str:
  token = _get_token()
  
  headers = {
    'authorization': f'Bearer {token}',
    'editor-version': 'vscode/1.100.3',
    'Content-Type': 'application/json',
  }
  
  body = {
    'messages': [
      {'role': 'user', 'content': text},
      {'role': 'system', 'content': 'You should answer only with the actual programming code'},
    ],
    'model': 'gpt-4.1',
    'temperature': 0,  # more deterministic response
  }
  
  if custom_body:
    body = custom_body
  
  url = 'https://api.githubcopilot.com/chat/completions'
  print(f'{url} :: {body["messages"]}')
  response = requests.post(url, headers=headers, json=body)
  
  print()
  print(response.status_code)
  print(response.headers)
  print()
  
  if response.status_code > 300:
    print(response.text)
    return None
  
  with open('.copilot.response.txt', 'w', encoding='utf8') as f:
    f.write(response.text)
  
  with open('.copilot.response.json', 'w', encoding='utf8') as f:
    json.dump(response.json(), f, indent=2)
  
  result = None
  
  choices = response.json().get('choices')
  if choices:
    try:
      result = choices[0]['message']['content']
    except KeyError:
      pass
  
  if result:
    with open('.copilot.content.txt', 'w', encoding='utf8') as f:
      f.write(result)

  return result


def get_models():
  token = _get_token()

  headers = {
    'authorization': f'Bearer {token}',
    'editor-version': 'vscode/1.100.3',
    'Content-Type': 'application/json',
  }
  
  url = 'https://api.githubcopilot.com/models'
  print(url)
  response = requests.get(url, headers=headers)
  
  print(response.status_code)
  
  if response.status_code != 200:
    print(response.text)
    return None
  
  print(response.json())
  print()
  
  with open('.copilot.response.json', 'w', encoding='utf8') as f:
    json.dump(response.json(), f, indent=2)
  
  data = response.json()['data']
  models = sorted([item['id'] for item in data])
  return models


def main():
  # Action 1
  text = 'code for date parsing function'
  result = get_completions(text=text)
  
  # Action 2
  body = {
    "messages": [
      {
        "role": "system",
        "content": 'The user needs help to write some new code.\nRespond only with a code block in java.\nAdd proper javadoc comments for methods signatures.\nUse indentation equal to 2 spaces.\nIn the multi-block structures, like "if-else", "try-catch" etc., the start of each block should be on its own line, as in ```if (condition) {\n}\nelse {\n}\nelse{\n}\n```.'
      },
      {
        "role": "user",
        "content": "code for b-tree indexing algorithm with examples"
      }
    ],
    "model": "gpt-4o",
    "temperature": 0.1,
    "n": 1
  }
  result = get_completions(custom_body=body)
  
  # Action 3
  result = get_models()
  print(result)


main()
