import requests
from bs4 import BeautifulSoup

root_url = ''

r = requests.get('https://www.dcard.tw/f/mood/p/234511181/b/1')
print(r)

# use find & find_all fountion
# spans = soup.find_all('span', class_='listTitle')
# for span in spans:
#     href = span.find('a').get('href')
#     url = root_url + href
#     if '796-59l9' == href:
#         break
#     print(f'{span.text}\n{url}\n')


# use select fountion
# for span in soup.select('span.listTitle'):
#     href = span.find('a').get('href')
#     url = root_url + href
#     if '796-59l9' == href:
#         break
#     print(f'{span.text}\n{url}\n')


# use CSS selector
# for span in soup.select('#list .listTitle'): 
#     # #+id名、class 搭配. 用空格分開
#     href = span.find('a').get('href')
#     url = root_url + href
#     if '796-59l9' == href:
#         break
#     print(f'{span.text}\n{url}\n')
