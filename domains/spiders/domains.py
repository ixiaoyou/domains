#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import scrapy
import json
import pymongo
import time
import datetime
from domains.items import DomainsItem

class MongoOperator:

    # 初始化mongo连接
    def __init__(self, uri='', db_name='domains', default_collection='domains'):
        self.client = pymongo.MongoClient(host=uri,retryWrites=False)
        self.db = self.client[db_name]
        self.collection = self.db[default_collection]

    def save(self, item):
        return self.collection.save(item)

    def close(self):
        self.client.close()



class domains(scrapy.Spider):
    name = "domains"
    start_urls = ["https://dnpedia.com/tlds/ajax.php?cmd=added&columns=id,name,length,idn,thedate,&ecf=zoneid,thedate&ecv=1,2020-05-05&zone=com&_search=false&nd=1588748974372&rows=500&page=1&sidx=length&sord=asc"]
    url = "https://dnpedia.com/tlds/ajax.php?cmd=added&columns=id,name,length,idn,thedate,&ecf=zoneid,thedate&ecv=1,%s&zone=com&_search=false&nd=%s&rows=500&page=%s&sidx=length&sord=asc"
    pageNo = 1
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'Content-Type': 'text/html; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Referer': 'https://dnpedia.com/tlds/daily.php',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'TLD-Selection=com;PHPSESSID=a4t71vf63pv1qg77tdr7aflvle;_jsuid=1702690357',
        'Host':'dnpedia.com'
    }
    allowed_domains = ['dnpedia.com']

    #时间戳
    timestemp = int(round(time.time() * 1000))
    #当前日期
    dt=datetime.datetime.now().strftime('%Y-%m-%d')

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url % (self.dt,self.timestemp,self.pageNo),headers=self.headers,method='GET',
            formdata={
                'cmd': 'added',
                'columns': 'id,name,length,idn,thedate,',
                'ecf': 'zoneid,thedate',
                'ecv': '1,%s' % self.dt,
                'zone': 'com',
                '_search': 'false',
                'nd': '%s' % self.timestemp,
                'rows': '500',
                'page': '1',
                'sidx': 'length',
                'sord': 'as'
            },callback=self.parse
        )

    def parse(self, response):
        results = json.loads(response.body)
        rows = results.get("rows")
        for row in rows:
            item=DomainsItem()
            item['name']=row.get('name')
            item['thedate'] = row.get('thedate')
            yield item
        total=int(results.get("total"))
        time.sleep(5)
        if self.pageNo < total:
            self.pageNo = self.pageNo + 1
            yield scrapy.FormRequest(
                url=self.url % (self.dt,self.timestemp,self.pageNo), headers=self.headers, method='GET',
                formdata={
                    'cmd': 'added',
                    'columns': 'id,name,length,idn,thedate,',
                    'ecf': 'zoneid,thedate',
                    'ecv': '1,%s' % self.dt,
                    'zone': 'com',
                    '_search': 'false',
                    'nd': '%s' % self.timestemp,
                    'rows': '500',
                    'page': '1',
                    'sidx': 'length',
                    'sord': 'as'
                }, callback=self.parse
            )

