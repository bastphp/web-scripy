import scrapy
from scrapy.http import Request

from webedu.items import ArticleItemLoader, WebeduItem
from urllib.parse import urlparse
import hashlib


def item_lod_detail(response):
    item_loader = ArticleItemLoader(item=WebeduItem(), response=response)
    item_loader.add_css("title", "title::text")
    item_loader.add_css("keywords", "meta[name='keywords']::attr(content)")
    item_loader.add_css("description", "meta[name='description']::attr(content)")
    item_loader.add_css("content_text", "#contentText p::text")
    item_loader.add_value('url', response.url)
    path = urlparse(response.url)
    m = hashlib.md5()
    m.update(path.path.encode('utf-8'))
    name = m.hexdigest() + '.html'
    fo = open(name, 'w')
    fo.write(response.text)
    fo.close()
    item_loader.add_value("html", name)
    return item_loader


class XuexilaSpider(scrapy.Spider):
    name = 'xuexila'
    allowed_domains = ['www.xuexila.com']
    start_urls = ['https://www.xuexila.com/']

    def parse(self, response):
        url_list = response.css('.nav_box .wrap .link_top a')
        for url_nods in url_list:
            url = url_nods.css('a::attr(href)').extract_first("")
            request_url = 'https:' + url
            yield Request(request_url, callback=self.parse_item)

    def parse_item(self, response):
        box = response.css('.wrap .box .abox_list')
        for box_node in box:
            url = box_node.css('.c11 .h_title a::attr(href)').extract_first("")
            if url:
                request_url = "https:" + url
                yield Request(request_url, callback=self.parse_item_detail)

    def parse_item_detail(self, response):
        # item_loader = ArticleItemLoader(item=WebeduItem(), response=response)
        # item_loader.add_css("title", "title::text")
        # item_loader.add_css("keywords", "meta[name='keywords']::attr(content)")
        # item_loader.add_css("description", "meta[name='description']::attr(content)")
        # item_loader.add_css("content_text", "#contentText p::text")
        # item_loader.add_value('url', response.url)
        # path = urlparse(response.url)
        # m = hashlib.md5()
        # m.update(path.path.encode('utf-8'))
        # name = m.hexdigest() + '.html'
        # fo = open(name, 'w')
        # fo.write(response.text)
        # fo.close()
        # item_loader.add_value("html", name)
        item_loader = item_lod_detail(response)
        page = response.css(".wrap .upnext ul li")
        for page_node in page:
            url = page_node.css("a::attr(href)").extract_first("")
            is_next = page_node.css("li::attr(class)").extract_first("")
            if url:
                request_url = "https:" + url
                if is_next == 'article_left':
                    yield Request(request_url, callback=self.parse_item_detail_up)
                else:
                    yield Request(request_url, callback=self.parse_item_detail_down)

        yield item_loader.load_item()

    def parse_item_detail_up(self, response):
        # item_loader = ArticleItemLoader(item=WebeduItem(), response=response)
        # item_loader.add_css("title", "title::text")
        # item_loader.add_css("keywords", "meta[name='keywords'] meta::attr(content)")
        # item_loader.add_css("description", "meta[name='description'] meta::attr(content)")
        # item_loader.add_css("content_text", "#contentText p::text")
        # item_loader.add_value('url', response.url)
        # path = urlparse(response.url)
        # m = hashlib.md5()
        # m.update(path.path.encode('utf-8'))
        # name = m.hexdigest() + '.html'
        # fo = open(name, 'w')
        # fo.write(response.text)
        # fo.close()
        # item_loader.add_value("html", name)
        item_loader = item_lod_detail(response)
        page = response.css(".wrap .upnext ul li")
        for page_node in page:
            url = page_node.css("a::attr(href)").extract_first("")
            is_next = page_node.css("li::attr(class)").extract_first("")
            if url:
                request_url = "https:" + url
                if is_next == 'article_left':
                    yield Request(request_url, callback=self.parse_item_detail_up)
        yield item_loader.load_item()

    def parse_item_detail_down(self, response):
        # item_loader = ArticleItemLoader(item=WebeduItem(), response=response)
        # item_loader.add_css("title", "title::text")
        # item_loader.add_css("keywords", "meta[name='keywords'] meta::attr(content)")
        # item_loader.add_css("description", "meta[name='description'] meta::attr(content)")
        # item_loader.add_css("content_text", "#contentText p::text")
        # item_loader.add_value('url', response.url)
        # path = urlparse(response.url)
        # m = hashlib.md5()
        # m.update(path.path.encode('utf-8'))
        # name = m.hexdigest() + '.html'
        # fo = open(name, 'w')
        # fo.write(response.text)
        # fo.close()
        # item_loader.add_value("html", name)
        item_loader = item_lod_detail(response)
        page = response.css(".wrap .upnext ul li")
        for page_node in page:
            url = page_node.css("a::attr(href)").extract_first("")
            is_next = page_node.css("li::attr(class)").extract_first("")
            if url:
                request_url = "https:" + url
                if is_next == 'article_right':
                    yield Request(request_url, callback=self.parse_item_detail_down)

        yield item_loader.load_item()
