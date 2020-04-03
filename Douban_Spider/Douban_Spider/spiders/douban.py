# -*- coding: utf-8 -*-
"""
获取豆瓣电影排行榜所有评论
豆瓣电影排行榜url: https://movie.douban.com/chart
"""

import scrapy
import re
from copy import deepcopy


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/']

    def parse(self, response):
        item = {}
        movie_class = response.xpath("//div/table").extract()
        for movie in movie_class:
            pattern = r'href="(.*?)">(.*?)</a>'
            result = re.findall(pattern, movie)
            for i in result:
                item['movie_name'] = i[1]
                item['movie_href'] = i[0]

                # 访问详情页
                yield scrapy.Request(
                    url=item['movie_href'],
                    callback=self.parse_url,
                    meta={"item": deepcopy(item)}
                )

    def parse_url(self, response):
        """ 单部电影详情页面 """
        item = response.meta.get('item')    # 取出值
        item['movie_grade'] = response.xpath('//div[@class="rating_wrap clearbox"]/div[2]/strong/text()').extract_first()
        try:
            item['movie_page_href'] = response.xpath("//div[@id='hot-comments']/a/@href").extract_first()
            item['movie_page_href'] = item['movie_href'] + item['movie_page_href']      # 构建评论页
        except TypeError as e:
            item['movie_page_href'] = response.xpath("//div[@class='mod-hd']/h2/span[@class='pl']/a/@href").extract_first()
        # 获取评论
        yield scrapy.Request(
            url=item['movie_page_href'],
            callback=self.parse_page_url,
            meta={"item": deepcopy(item)}
        )

    def parse_page_url(self, response):
        """ 获取每个人评论 """
        item = response.meta.get('item')  # 取出值
        comment_list = response.xpath("//div[@class='comment-item']")
        for com in comment_list:
            item['user_author'] = com.xpath('.//span[@class="comment-info"]/a/text()').extract_first()
            item['user_grade'] = com.xpath('.//span[@class="comment-info"]/span[2]/@title').extract_first()
            item['user_comment'] = com.xpath('.//span[@class="short"]/text()').extract_first()    # 评论
            # print('=' * 30)
            yield item

        # 评论下一页
        # next_url = response.xpath("//a[@class='next']/@href").extract_first()
        # next_url = item['movie_page_href'][:-24] + next_url
        # yield scrapy.Request(
        #     url=next_url,
        #     callback=self.parse_page_url,
        #     meta={"item":deepcopy(item)}
        # )
