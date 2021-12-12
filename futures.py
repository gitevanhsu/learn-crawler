import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pprint import pprint

def crawl(date):
    print('crawling', date.strftime('%y/%m/%d'))
    url = 'https://www.taifex.com.tw/cht/3/futContractsDate'
    sorce = f'queryDate={date.year}%2F{date.month}%2F{date.day}'
    data=[] # 用於儲存資料

    r = requests.get(url+'?'+sorce)
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, 'lxml')
    else:
        print('connettion error')

    try:
        table = soup.find('table', class_='table_f')
        trs = table.find_all('tr')
    except AttributeError:
        print('No data for', date.strftime('%y/%m/%d'))
        return

    rows = trs[3:]
    data = {}

    for row in rows:
        ths = row.find_all('th')
        tds = row.find_all('td')
        tds = ths+tds
        cells = [td.text.strip() for td in tds]

        if cells[0] == '期貨小計':
            break

        if len(cells) == 15:
            product = cells[1]
            row_data = cells[1:]
        else:
            row_data = [product] + cells

        # print(len(data))

        converted = [int(d.replace(',', '')) for d in row_data[2:]]
        row_data = row_data[:2]+converted
        # print(row_data)

        headers = ['商品', '身份別', '交易多方口數', '交易多方金額', '交易空方口數', '交易空方金額', '交易多空淨口數', '交易多空淨額'
                    , '未平倉多方口數', '未平倉多方金額', '未平倉空方口數', '未平倉空方金額','未平倉多空淨口數', '未平倉多空淨額']

        # dict format product > who > what
        product = row_data[0]
        who = row_data[1]
        contents = {headers[i]: row_data[i] for i in range(2, len(headers))}

        if product not in data:
            data[product] = {who:contents}
        else:
            data[product][who] = contents

    print('臺股期貨,外資,未平倉多空淨額:', data['臺股期貨']['外資']['未平倉多空淨額'])
    # pprint(data)
    return data



date = datetime.today()
while True:
    crawl(date)
    date = date - timedelta(days=1)
    if date < datetime.today() - timedelta(days=30):
        break

