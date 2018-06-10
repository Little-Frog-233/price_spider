#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 09:23:00 2018

@author: ruicheng
"""

import requests
from pyquery import PyQuery as pq
import json
import time

base_url = 'http://watch.xbiao.com/rolex/10000129/p%d.html'
path = '/Users/ruicheng/Documents/上海师范研究生/python相关/爬虫/腕表之家爬虫/劳力士爬虫/劳力士宇宙计型迪通拿价格.txt'

def get_page(page):
    url = base_url%page
    try:
        response = requests.get(url)
        if response.status_code == 200:
            #print('网页编码为:',response.encoding)
            response.encoding = 'utf-8'
            #print('网页编码改为:',response.encoding)
            return response.text
        else:
            return None
    except requests.ConnectionError as e:
        print('Error',e.args)
        
def price(html):
    result1 = []
    result2 = []
    result3 = []
    if html:
        doc = pq(html)
        results_money = doc('.money').items()
        results_pic = doc('.watch-pic img').items()
        for money in results_money:
            result1.append(money.text())
        for pic in results_pic:
            result2.append(pic.attr('src'))
            result3.append(pic.attr('alt'))
        for i in range(len(result1)):
            price = {}
            price['name'] = result3[i]
            price['img'] = result2[i]
            price['money'] = result1[i]
            yield price

def save_result(results):
    for result in results:
        with open(path,'a',encoding='utf-8') as f:
            f.write(json.dumps(result,ensure_ascii=False)+'\n')

if __name__ == '__main__':
    for page in range(1,4):
        html = get_page(page)
        results = price(html)
        save_result(results)
        time.sleep(1)
    
    