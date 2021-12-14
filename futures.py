import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import json
import time


def crawl(date):
    print('crawling', date.strftime('%y-%m-%d'))
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
        print('No data for', date.strftime('%y-%m-%d'))
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

    return data, date



def save_future(data, date):
    
    json_data = json.dumps(data, ensure_ascii=False, indent=1)
    path = 'downloads/json_futures/'
    filename = '{}future_{}.json'.format(path, date.strftime('%Y-%m-%d'))

    with open(filename,'w') as f:
        f.write(json_data)
        print('save future json file {}'.format(date.strftime('%Y-%m-%d')))    


def main():
    start = time.time()
    date = datetime.today()
    futures =[]

    with ProcessPoolExecutor(max_workers=16) as executor:
        while True:
            future = executor.submit(crawl, date)
            futures.append(future)

            date = date - timedelta(days=1)
            if date < datetime.today() - timedelta(days=730):
                break

        for future in as_completed(futures):
            if future.result() == None:
                print(date.strftime('%Y-%m-%d'),'no future data')
            else:
                data ,date = future.result()
                save_future(data, date)


    end = time.time()
    print(f'下載資料共花費{end - start}秒')

if __name__ == "__main__":
    main()




