# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UsersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    avatar_url =scrapy.Field()
    badge = scrapy.Field()
    follower_count = scrapy.Field()
    gender = scrapy.Field()
    headline = scrapy.Field()
    is_advertiser = scrapy.Field()
    is_followed = scrapy.Field()
    is_following = scrapy.Field()
    is_org = scrapy.Field()
    type = scrapy.Field()
    url = scrapy.Field()
    url_token = scrapy.Field()
    user_type = scrapy.Field()
    pass
