import scrapy
from alyun.items import AlyunItem
from scrapy import Request


class AlixiaoSpider(scrapy.Spider):
    name = 'alixiao'
    allowed_domains = ['alixiaozhan.net']
    start_urls = [
        'https://alixiaozhan.net/api/discussions?include=user%2ClastPostedUser%2Ctags%2Ctags.parent%2CfirstPost&sort=']

    def parse(self, response):
        _data = response.json()
        item = AlyunItem()
        item['link_next'] = _data['links']['next']
        _next = _data['links']['next']
        for data in _data['data']:
            item['tag'] = data['relationships']['tags']['data'][0]["id"]
            item['title'] = data['attributes']["title"]
            item['create_time'] = data['attributes']['createdAt']
            item['Id'] = data["id"]
            item['del_url'] = "https://alixiaozhan.net/d/{}".format(str(item['Id']))
            print(f"link_next", _next)
            # 详情页
            yield Request(item['del_url'], callback=self.parse_detail, meta={'item': item}, priority=10,
                          dont_filter=True)
            # 翻页
            yield Request(url=_next, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta["item"]
        # print(f"这是详情的", item["del_url"])
        # html = response
        # html = BeautifulSoup(response.content)
        div = response.xpath(".//div[@class='Post-body']").extract()
        _href = response.xpath(".//div[@class='Post-body']//p/a/@href").extract()
        item["context"] = div
        item['yun_href'] = _href
        yield item
