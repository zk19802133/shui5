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
            items=self.make_requests_from_url(url).replace(callback=self.parse_list)
            totalitem.append(items)
        return totalitem

    def parse_list(self,response):
        items=[]
        hxs2=HtmlXPathSelector(response)
        newurls=hxs2.select('//h1/a[2]/@href').extract()
        #unsolved start
        flag=hxs2.select('//td[@class="page_links"]/b/u/text()').extract()[0]
        page_links=hxs2.select('//td[@class="page_links"]/a[@title>'+flag+']/@href').extract()
        for page_link in page_links:
            page_link="http://www.shui5.cn"+page_link
            items.extend(self.make_requests_from_url(page_link))
        #unsolved end
        for url in newurls:
            url="http://www.shui5.cn"+url
            print "url--------<"+url+">--------"
            # item=Request(url, callback=self.parse_article)
            item=self.make_requests_from_url(url).replace(callback=self.parse_article)
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
