import re
import copy
import json
import scrapy

from urllib import parse as urllib_parse


class InsiderSpider(scrapy.Spider):
    name = 'insider'
    allowed_domains = ['insider.com']
    # python在params转化的时候会把 空格 符号转化为 + 符号，因此在此提前将空格改为网页默认编码 %20
    keyword_list = ["investments%20advisor", "investment%20planning", "investment%20plan"]
    start_urls = ['https://www.insider.com/s']
    url = "https://www.insider.com/s"
    params_dict = {
        "templateId": "river",
        "json": "1",
        "q": "investment plan",     # query keyword 检索关键词
        "p": "0",   # page 检索页
        "page[limit]": "20",    # page_limit 每页的条数
        "globalIndex": "1"
    }

    def start_requests(self):
        for keyword in self.keyword_list:
            # 深拷贝
            params_dict = copy.deepcopy(self.params_dict)
            params_dict["q"] = keyword
            params_dict_string = urllib_parse.urlencode(params_dict)
            # url = self.url + "?" + params_dict_string
            url = "{url}?{params_dict_string}".format(url=self.url, params_dict_string=params_dict_string)
            yield scrapy.FormRequest(url=url,
                                     # formdata=params_dict,
                                     method="get",
                                     dont_filter=True)
            break

    def parse(self, response):
        print(response.text)
        json_data = json.loads(response.text)
        # print(response.text)
        blog_url_re_rule = r'<img src=\"(.*?)"'  # 正则规则
        blog_url_list = re.findall(blog_url_re_rule, json_data['rendered'])
        print(blog_url_list)



# 直接调用scrapy，适合本地开发环境使用
if __name__ == '__main__':
    from scrapy import cmdline
    args = "scrapy crawl insider".split()
    cmdline.execute(args)
