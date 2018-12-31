# -*- coding: utf-8 -*-
import json
import sys
sys.path.append(r'D:\python_ptc\scrapy_project\zhihuus\zhihuusers\spiders\zhihu')
from scrapy import Spider,Request
from zhihuusers.items import UsersItem

class ZhihuSpider(Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    start_user = 'excited-vczh'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'
    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(self.user_url.format(user=self.start_user,include=self.user_query),callback=self.parse_user)
        yield Request(self.follows_url.format(user=self.start_user,include=self.follows_query,offset=20,limit=20),callback=self.parse_follows)

    def parse_user(self, response):
        result = json.loads(response.text)
        item = UsersItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item

        yield Request(self.follows_url.format(user=result.get('url_token'),include=self.follows_query,limit=20,offset=0),self.parse_follows)

    def parse_follows(self,response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                yield Request(self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.parse_user)
            if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
                total = results.get('paging').get('totals')
                us=lambda x: x*20
                for i in range ((total//20)+1):
                    off_set=us(i)
                    next_page ='https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'

                    yield Request(next_page.format(user=self.start_user,include=self.follows_query,offset=off_set,limit=20),self.parse_follows)
