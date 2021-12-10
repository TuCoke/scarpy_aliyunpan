import scrapy
from alyun.items import AlyunItem
from scrapy import Request


class aliyunshareSpider(scrapy.Spider):
    name = 'aliyunshare'
    allowed_domains = ['aliyunshare.org']
    start_urls = [
        'https://aliyunshare.org/api/discussions?include=user%2ClastPostedUser%2Ctags%2Ctags.parent%2CfirstPost&sort=&page%5Boffset%5D=20']

    # 浏览器用户代理
    headers = {
        "cookie": "__51vcke__JWPJL2zENFklfOta=8d07ca25-9279-5fe5-b126-01196a5b0a14; __51vuft__JWPJL2zENFklfOta=1638753210744; flarum_remember=evF45KEdA08cK0kX2OCZu7sGHyaCOjig3Hnrc4ZG; flarum_session=uERWrFFc15dwTtfjeyLVC6IkCxFhGU74YjYC666G; __51uvsct__JWPJL2zENFklfOta=3; __vtins__JWPJL2zENFklfOta=%7B%22sid%22%3A%20%22d5d31870-8630-5c21-8890-e39de6a00742%22%2C%20%22vd%22%3A%208%2C%20%22stt%22%3A%20168667%2C%20%22dr%22%3A%2035228%2C%20%22expires%22%3A%201638857542122%2C%20%22ct%22%3A%201638855742122%7D",
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    # 指定cookies
    cookies = {
        'cookie': '__51vcke__JWPJL2zENFklfOta=8d07ca25-9279-5fe5-b126-01196a5b0a14; __51vuft__JWPJL2zENFklfOta=1638753210744; flarum_remember=evF45KEdA08cK0kX2OCZu7sGHyaCOjig3Hnrc4ZG; flarum_session=uERWrFFc15dwTtfjeyLVC6IkCxFhGU74YjYC666G; __51uvsct__JWPJL2zENFklfOta=3; __vtins__JWPJL2zENFklfOta=%7B%22sid%22%3A%20%22d5d31870-8630-5c21-8890-e39de6a00742%22%2C%20%22vd%22%3A%208%2C%20%22stt%22%3A%20168667%2C%20%22dr%22%3A%2035228%2C%20%22expires%22%3A%201638857542122%2C%20%22ct%22%3A%201638855742122%7D',
    }

    def parse(self, response):
        _data = response.json()
        item = AlyunItem()
        item['link_next'] = _data['links']['next']
        _prev = _data['links']['prev']
        _next = _data['links']['next']
        for data in _data['data']:
            item['tag'] = data['relationships']['tags']['data'][0]["id"]
            item['title'] = data['attributes']["title"]
            item['create_time'] = data['attributes']['createdAt']
            item['Id'] = data["id"]
            item['del_url'] = "https://aliyunshare.org/d/{}".format(str(item['Id']))
            print(f"link_next", _next)
            # 详情页
            yield Request(item['del_url'], headers=self.headers, cookies=self.cookies, callback=self.parse_detail,
                          meta={'item': item}, priority=10,
                          dont_filter=True)
            # 翻页
            yield Request(url=_prev, headers=self.headers, cookies=self.cookies, callback=self.parse)
            yield Request(url=_next, headers=self.headers, cookies=self.cookies, callback=self.parse)

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
