# Downloads a page with Google search results,
# parses the HTML and prints the resulting URLs


import urllib.parse as urllib
import lxml.html as lxml
import requests
import os


SEARCH_TERM = 'fringe'
NUM = 20
LANG = 'en'

out_file = 'google_{}.html'.format(SEARCH_TERM)


url = "https://www.google.com/search?q={}&num={}&hl={}".format(SEARCH_TERM, NUM, LANG)
print('==============\n' + url)

raw = requests.get(url).text
page = lxml.fromstring(raw)

if os.path.exists(out_file):
  filenum = 1
  while os.path.exists(out_file + '.' + str(filenum)):
    filenum += 1
  out_file += '.' + str(filenum)
print('FILE: {}'.format(out_file))
print('==============\n')

with open(out_file, 'w') as f: f.write(raw)

for result in page.cssselect(".kCrYT > a"):
  url = result.get("href")
  if url.startswith("/url?"):
    url = urllib.parse_qs(urllib.urlparse(url).query)['q']
    print(url[0])
