# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http.response import Request
from ..items import InsItem


class InsSpider(scrapy.Spider):
    name = 'ins'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/graphql/query/?query_hash=ecd67af449fb6edab7c69a205413bfa7&variables={"first":24}']

    def parse(self, response):
        res = json.loads(response.text)
        data = res.get('data')
        user = data.get('user')
        edge_web_discover_media = user.get('edge_web_discover_media')
        edges = edge_web_discover_media.get('edges')
        for x in edges:
            node = x.get('node')
            shortcode = node.get('shortcode')
            url = 'https://www.instagram.com/p/{}/?__a=1'.format(shortcode)
            # 进入二级页面 准备找到个人主页的链接
            yield Request(
                url=url,
                callback = self.parse_detial
            )
            break

    def parse_detial(self,response):
        res = json.loads(response.text)
        graphql = res.get('graphql')
        shortcode_media = graphql.get('shortcode_media')
        owner = shortcode_media.get('owner')
        username = owner.get('username')
        personal_url = 'https://www.instagram.com/{}/?__a=1'.format(username)
        # 拼接出个人主页的链接
        yield Request(
            url=personal_url,
            meta={'username':username},
            callback=self.parse_person
        )

    def parse_person(self,response):
        username = response.meta.get('username')
        res = json.loads(response.text)
        graphql = res.get('graphql')
        user = graphql.get('user')
        # 找到查看粉丝请求链接
        # id = user.get('id')
        # fans_url = 'https://www.instagram.com/graphql/query/?query_hash=56066f031e6239f35a904ac20c9f37d9&variables={"id":"{}","include_reel":true,"fetch_mutual":false,"first":24}'.format(id)
        # yield Request(
        #     url=fans_url,
        #     callback=self.parse_fans
        # )

        # 找到每个帖子的请求链接
        edge_owner_to_timeline_media = user.get('edge_owner_to_timeline_media')
        edges = edge_owner_to_timeline_media.get('edges')
        for x in edges:
            node = x.get('node')
            shortcode = node.get('shortcode')
            post_url = 'https://www.instagram.com/p/{}/?__a=1'.format(shortcode)
            yield Request(
                url=post_url,
                meta={'username': username},
                callback=self.prase_post
            )


    def prase_post(self,response):
        # 作者名称
        username = response.meta.get('username')
        print(username)

        res = json.loads(response.text)
        graphql = res.get('graphql')
        shortcode_media = graphql.get('shortcode_media')
        is_video = str(shortcode_media.get('is_video'))

        # 判断是不是图片 若是保存图片，评论，找到id进入个人页面
        if is_video == 'False':
            # 图片地址
            display_url = shortcode_media.get('display_url')
            print(display_url)

            # 作者动态
            edge_media_to_caption = shortcode_media.get('edge_media_to_caption')
            edges = edge_media_to_caption.get('edges')[0]
            node = edges.get('node')
            text = node.get('text')
            text.replace('\n','').replace(' ','')
            print(text)
            print('..................')

            # 评论信息
            edge_media_to_comment = shortcode_media.get('edge_media_to_comment')
            edges = edge_media_to_comment.get('edges')
            comment = []
            for x in edges:
                node = x.get('node')
                text = node.get('text')
                comment.append(text)
            comment=';'.join(comment)
            if comment == '':
                comment = '无评论'
            print(comment)

            item = InsItem()
            item['username'] = username
            item['display_url'] = display_url
            item['text'] = text
            item['comment'] = comment
            yield item


    def parse_fans(self,response):
        response = json.loads(response.text)
        data = response.get('data')
        user = data['user']
        edge_followed_by = user['edge_followed_by']
        edges = edge_followed_by['edges']
        # 粉丝数据
        for user_name in edges:
            node = user_name['node']
            username = node['username']
            personal_url = 'https://www.instagram.com/{}/?__a=1'.format(username)
            # 拼接出粉丝个人主页的链接
            yield Request(
                url=personal_url,
                callback=self.parse_person
            )














