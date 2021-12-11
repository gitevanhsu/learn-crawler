import requests
from bs4 import BeautifulSoup

def main(url):
    school_count = dict() # 用字典將使用者(學校)出現次數儲存
    num = 0

    while True:
        error_time = 0
        num += 1
        r = requests.get(f'{url}/b/{num}') 
        print(num, r.status_code) # 記錄次數，確認網頁status
        
        if r.status_code == 200:
            error = 0 
            soup = BeautifulSoup(r.text, 'html.parser') # 解析網頁資訊
            school = soup.find('span', class_='cax7qe-2 hKAjCB').text # 搜尋使用者(學校)名稱
        else:
            # 留言刪除或是搜尋不到東西時紀錄次數，出現超過三次代表可能已無留言。
            error+=1
            if error == 3 :
                break

        # 記錄使用者(學校)出現次數,用字典儲存
        if school in school_count.keys(): 
            school_count[school] += 1
        else:
            school_count[school] = 1
        # if num == 20:
        #     break
    # 印出所有出現的使用者(學校)以及出現次數
    for _ in sorted(school_count.keys()):
            print(_,f'出現次數{school_count[_]}')

url = 'https://www.dcard.tw/f/mood/p/234511181'
if __name__ == '__main__':
    main(url)
