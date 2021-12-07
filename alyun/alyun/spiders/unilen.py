import scrapy
from alyun.items import AlyunItem
from scrapy import Request


class unilenSpider(scrapy.Spider):
    name = 'pan.unilei'
    allowed_domains = ['pan.unilei.cn']
    start_urls = [
        'https://pan.unilei.cn/api/discussions?include=user%2ClastPostedUser%2Ctags%2Ctags.parent%2CfirstPost&sort=']

    # 浏览器用户代理
    headers = {
        "cookie": "flarum_remember=KdEaSgWvEAxRqkw40Fb6i4oSrOMlVfjRf8WSNRWO; flarum_session=CG7iPCWHEANJg7IbWXh8xgiw3ITHK4gmDMUaWpL2",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    # 指定cookies
    cookies = {
        'cookie': 'flarum_remember=KdEaSgWvEAxRqkw40Fb6i4oSrOMlVfjRf8WSNRWO; flarum_session=CG7iPCWHEANJg7IbWXh8xgiw3ITHK4gmDMUaWpL2',
    }
    # # 重写start_requests方法
    # def start_requests(self):
    #     # 浏览器用户代理
    #     headers = {
    #         "cookie":"flarum_remember=KdEaSgWvEAxRqkw40Fb6i4oSrOMlVfjRf8WSNRWO; flarum_session=CG7iPCWHEANJg7IbWXh8xgiw3ITHK4gmDMUaWpL2",
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    #     }
    #     # 指定cookies
    #     cookies = {
    #         'cookie': 'flarum_remember=KdEaSgWvEAxRqkw40Fb6i4oSrOMlVfjRf8WSNRWO; flarum_session=CG7iPCWHEANJg7IbWXh8xgiw3ITHK4gmDMUaWpL2',
    #     }
    #
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse)

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
            item['del_url'] = "https://pan.unilei.cn/d/{}".format(str(item['Id']))
            print(f"link_next", _next)
            # 详情页
            yield Request(item['del_url'], headers=self.headers, cookies=self.cookies, callback=self.parse_detail, meta={'item': item}, priority=10,
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
