# -*- coding: utf-8 -*-
import json
import time

import scrapy

from zhihuser.items import ZhihuserItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']

    start_type = 'people'
    start_user = 'excited-vczh'
    user_url = 'https://www.zhihu.com/{type}/{user}/following'
    following_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follow_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    #请求网址
    def start_requests(self):
        #url='https://www.zhihu.com/people/excited-vczh/activities'
        yield scrapy.Request(
            self.user_url.format(type=self.start_type, user=self.start_user),
            callback=self.parse_use,dont_filter=True,priority=301)
        yield scrapy.Request(
            self.following_url.format(
                user=self.start_user,
                include=self.follow_query,
                offset=0,
                limit=20),
            callback=self.parse_follow, dont_filter=True,priority=305)

    '''
    def parse(self, response):
        print(response.text)
    '''
    #解析详细页
    def parse_use(self, response):
        name = response.css(
            '#ProfileHeader > div > div.ProfileHeader-wrapper > div > div.ProfileHeader-content > div.ProfileHeader-contentHead > h1 > span.ProfileHeader-name::text'
        ).extract_first()
        headline = response.css(
            '#ProfileHeader > div > div.ProfileHeader-wrapper > div > div.ProfileHeader-content > div.ProfileHeader-contentHead > h1 > span.RichText.ztext.ProfileHeader-headline::text'
        ).extract_first()
        domicile = response.css(
            '#ProfileHeader > div > div.ProfileHeader-wrapper > div > div.ProfileHeader-content  > div > div > div:nth-of-type(1) > div > span::text'
        ).extract()
        career = response.css(
            '#ProfileHeader > div > div.ProfileHeader-wrapper > div > div.ProfileHeader-content > div > div > div:nth-of-type(3)::text'
        ).extract()
        educational_experice = response.css(
            '#ProfileHeader > div > div.ProfileHeader-wrapper > div > div.ProfileHeader-content  > div > div > div:nth-of-type(1) > div:nth-of-type(2)::text'
        ).extract()
        individual_resume = response.css(
            'div.RichText:nth-of-type(2)::text').extract_first()
        #print(name, headline, domicile, career, educational_experice,individual_resume)
        item = {
            'name': name,
            'headline': headline,
            'domicile': domicile,
            'career': career,
            'educational_experice': educational_experice,
            'individual_resume': individual_resume
        }
        yield item
        #print('???????????????????????????????????')
    #下一页和写一个人以及他的好友的详细信息
    def parse_follow(self, response):
        results = json.loads(response.text)

        if 'data' in results.keys():
            for result in results.get('data'):
                yield scrapy.Request(
                    self.user_url.format(
                        type=self.start_type, user=result.get('url_token')),
                    callback=self.parse_use, dont_filter=True,priority=301)
                yield scrapy.Request(
                    self.following_url.format(
                        user=result.get('url_token'),
                        include=self.follow_query,
                        offset=0,
                        limit=20),
                    callback=self.parse_follow, dont_filter=True,priority=305)
        

        if 'paging' in results.keys() and results.get('paging').get(
                'is_end') == False:
            next_page = results.get('paging').get('next')
            yield scrapy.Request(next_page, callback=self.parse_follow, dont_filter=True,priority=305)
