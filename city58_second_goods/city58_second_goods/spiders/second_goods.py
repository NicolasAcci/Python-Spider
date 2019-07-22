# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from city58_second_goods.items import City58SecondGoodsItem, GoodsItem


class SecondGoodsSpider(scrapy.Spider):
    name = 'second_goods'
    # allowed_domains = ['允许爬取的域名'], 如果解析到的域名（url)不在这儿， 就不会发送该url
    allowed_domains = ['bj.58.com']
    start_urls = ['https://bj.58.com/sale.shtml']

    def parse(self, response):
        print("*" * 80)
        html = response.xpath('//div/ul/li/a/@href').extract()
        html.pop(0)
        # 获取二级页面url
        item = City58SecondGoodsItem()
        # print("1", html)
        for i in html[:4]:
            item["goods_url"] = i
            goods_url = "https:" + i
            print(goods_url, "jjjjjjjjjjjj")
            yield item
            yield scrapy.Request(url=goods_url, callback=self.goods_info)

    def goods_info(self, response):
        print("+" * 50)
        soup = BeautifulSoup(response.text, 'lxml')
        temp_title = soup.title.get_text()
        print("1" * 50, temp_title)
        title = temp_title.split(" - ")[0]
        try:
            temp_time = soup.select("div.detail-title__info > div")[0].get_text()
            #[0].get_text()用来提取文本内容
            time = temp_time.split(" ")[0]
            temp_price = soup.select("span.infocard__container__item__main__text--price")[0].get_text()
            price = temp_price.split()[0]
            temp = soup.select("div.infocard__container > div:nth-of-type(2) > div:nth-of-type(2)")[0].get_text()
            if '成新' in temp:
                color = temp
                temp_area = soup.select("div.infocard__container > div:nth-of-type(3) > div:nth-of-type(2)")[0]
            else:
                color = None
                temp_area = soup.select("div.infocard__container > div:nth-of-type(2) > div:nth-of-type(2)")[0]
            temp_area = list(temp_area.stripped_strings)
            area = list(filter(lambda x: x.replace("-", ''), temp_area))
            temp_cate = list(soup.select("div.nav")[0].stripped_strings)
            cate = list(filter(lambda x: x.replace(">", ''), temp_cate))
            item = GoodsItem()
            item['goods_title'] = title
            item['goods_time'] = time
            item['goods_price'] = price
            item['goods_color'] = color
            item['goods_area'] = str(area)
            item['goods_cate'] = str(cate)
            yield item
        except:
            print("Error 404!")
