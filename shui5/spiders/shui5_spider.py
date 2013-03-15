from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from shui5.items import Shui5Item
# from scrapy.http import Request

class Shui5Spider(BaseSpider):
    name = "shui5"
    allowed_domains = ["shui5.cn"]
    start_urls = [
        "http://www.shui5.cn/"
    ]

    def parse(self, response):
        totalitem=[]
        hxs=HtmlXPathSelector(response)
        theurls=hxs.select('//div[@class="category_body"]//a/@href').extract()
        for url in theurls:
            url="http://www.shui5.cn"+url
            print "url--------<"+url+">--------"
            area_items=self.make_requests_from_url(url).replace(callback=self.parse_list)
            totalitem.append(area_items)
        return totalitem

    def parse_list(self,response):
        area_items=[]
        hxs2=HtmlXPathSelector(response)
        page_links=[] # for next pages
        links=[] # for links in a page
        page_links.append(unicode(response.url))
        for thelink in hxs2.select('//td[@class="page_links"]/a/@href').extract():
            thelink="http://www.shui5.cn"+thelink
            page_links.append(thelink)
        for page_link in page_links:
            area_items.append(self.make_requests_from_url(page_link).replace(callback=self.parse_links))
        return area_items

    def parse_links(self,response):
        items=[]
        hxs4=HtmlXPathSelector(response)
        article_links=hxs4.select('//h1/a[2]/@href').extract()
        for article_link in article_links:
            article_link="http://www.shui5.cn"+article_link
            item=self.make_requests_from_url(article_link).replace(callback=self.parse_article)
            items.append(item)
        return items

    def parse_article(self,response):
        item=Shui5Item()
        hxs3=HtmlXPathSelector(response)
        item['title']=hxs3.select('//div[@class="main_title"]/center/text()').extract()[0]
        item['link']=unicode(response.url)
        content=hxs3.select('//table[@class="jump_page_box"]').extract()
        item['desc']=content[0]
        # item['desc']='test'
        # print response.body_as_unicode()
        return item
