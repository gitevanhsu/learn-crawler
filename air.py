import requests
import pprint
import re


r = requests.get('https://airtw.epa.gov.tw/json/camera_ddl_pic/camera_ddl_pic_2021121918.json')
if r.status_code == requests.codes.ok:
    data = r.json()
    # pprint.pprint(data)
    # print()

    for d in data:
        name = d['Name']
        if 'AQI' not in name:
            continue
        site_name, aqi = re.search(r'(.+)\(AQI=(\d*)', name).group(1, 2)    
        print(site_name, aqi)

    # name = [d for d in data if '花蓮' in d['Name']][0]['Name']
    # print(name)
    # print()

    # site_name, aqi = re.search(r'(.+)\(AQI=(\d*)', name).group(1, 2)
    # print(site_name, aqi)

