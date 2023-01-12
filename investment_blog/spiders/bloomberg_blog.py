# -*- coding: utf-8 -*-

import re
import copy
import json
import scrapy
from investment_blog.settings import FILES_STORE
from investment_blog.items import DownloadFilesItem

# 默认video的size大小，列表中的元素值越大，视频大小越大
VIDEO_SIZE_LIST = ['64', '150', '400', '600', '800', '1200', '2400', '3000', '5000']

# 下载video的大小参数，如果选择的大，则应该调大 scrapy的 DOWNLOAD_TIMEOUT 参数
VIDEO_SIZE = '150'


# bloomberg的请求header，其中cookie是必要的，必须有cookie才能访问api
SEARCH_HEADER = {
    'authority': 'www.bloomberg.com',
    'accept': '*/*',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'cookie': 'seen_uk=1; geo_info={%22country%22:%22HK%22%2C%22region%22:%22Asia%22%2C%22fieldN%22:%22hf%22}|1674028054669; _sp_krux=false; _sp_v1_ss=1:H4sIAAAAAAAAAItWqo5RKimOUbLKK83J0YlRSkVil4AlqmtrlXRGldFSWSwAQNXmRIcBAAA%3D; _sp_su=false; agent_id=5fc836e4-4e96-4f0f-91a8-c8e360791294; session_id=fa363455-73a5-4b41-b0f7-4bbc8ec1c958; session_key=ace6ac34c363e8844be2b43e3de85118949846a8; gatehouse_id=a3055b7c-0630-4642-ab08-d1ac951eef74; geo_info=%7B%22countryCode%22%3A%22HK%22%2C%22country%22%3A%22HK%22%2C%22field_n%22%3A%22hf%22%2C%22trackingRegion%22%3A%22Asia%22%2C%22cacheExpiredTime%22%3A1674028055625%2C%22region%22%3A%22Asia%22%2C%22fieldN%22%3A%22hf%22%7D%7C1674028055625; _reg-csrf=s%3A0h-4eTUy521OW2laefzDDgY9.78ITKibcFswhgxFvR8pZ320%2Fw%2BZ0o660tEfD%2Fj%2Fjp7s; ccpaUUID=1cebfddf-d4c6-4f85-95e4-dcaac166a672; dnsDisplayed=true; ccpaApplies=true; signedLspa=false; bbgconsentstring=req1fun1pad1; _gcl_au=1.1.1766585381.1673423257; bdfpc=004.4717878102.1673423257119; pxcts=37c5fb53-9184-11ed-8a25-6d475a516a58; _pxvid=37c5ee35-9184-11ed-8a25-6d475a516a58; _gid=GA1.2.1709172328.1673423258; ln_or=eyI0MDM1OTMiOiJkIn0%3D; _rdt_uuid=1673423263097.6f8f91a4-7616-4388-8d3e-3f0b70306d7e; _cc_id=d91291962b4a509db5f951a3bcb9b6f2; _fbp=fb.1.1673423265360.691557448; _schn=_n0447zg; _scid=33e5be9b-e7a2-4d62-a300-96afcaaf3843; _li_dcdm_c=.bloomberg.com; _lc2_fpi=b1166d620485--01gpfwsf2eqj41n8ssh9d5y20f; _sctr=1|1673366400000; trc_cookie_storage=taboola%2520global%253Auser-id%3Da4bff76b-daf7-461e-8229-a2155abb6089-tuctab02764; exp_pref=APAC; _uetsid=3acb5300918411eda5b923b2dbd391e0; _uetvid=3acb7620918411ed93b22b315d112156; panoramaId_expiry=1673511253217; __sppvid=e6c94294-b9c5-4451-a2aa-7ad0a4f495a5; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.bloomberg.com/markets%22%2C%22sref%22:%22%22%2C%22sts%22:1673430396229%2C%22slts%22:1673423265385}; _parsely_visitor={%22id%22:%22pid=91c3b74938fa3014546b1da8f78f560b%22%2C%22session_count%22:2%2C%22last_session_ts%22:1673430396229}; _gat_UA-11413116-1=1; _px3=5599d6c9334e8ea7c51b490c720f71a3e6b73070d197dd1674391a6054b4d342:3d8dQO30Rc8I9JI6aekxmKCzQPJnTlCS9BJRNXFXchHt40bBvThkNqbqhAfgLv06dAjV+2fynKN1xD3WXJBIEQ==:1000:ISjhhpMaq0nS/fpL9VU9v+uM/mYbvvNM8I3TYm1QahPYBrUSxsurREDO5R5F9D42SW4+Tc+Dk3WW0rDABwjQHbzMTqZ2CPYKnT/Zrg80GaEpVBNG0Cwv8Z1Y1uwvu0CRGPsPy6MZNGZV8A0UVI48hi6rrXTBLoovlSPFiw/2YUkwIQyb9dGz3Fzb5tu0qddZ2VHmffb3QpP4OJ1Rj4e8mw==; _px2=eyJ1IjoiNmUwZWM2MTAtOTE5NS0xMWVkLTg2OTctM2IwYWRkYTY3MmUxIiwidiI6IjM3YzVlZTM1LTkxODQtMTFlZC04YTI1LTZkNDc1YTUxNmE1OCIsInQiOjE2NzM0MzA5NTEyMTgsImgiOiIwMDFmMWY5M2EwNGI3NTRiZDMzN2U5ZDM3MTMwMTI3YzRjZDkwMDBhMmQ4YTc5NWQ3ZTZiZTYxNWU0MGNlYzQwIn0=; _reg-csrf-token=gimOfyV4-u-CesCpPnSFQTi8WYKKu3Fwhvog; _user-data=%7B%22status%22%3A%22anonymous%22%7D; _last-refresh=2023-1-11%209%3A50; _sp_v1_uid=1:29:75401edf-1b67-47cc-a487-cb79a5bdc9e9; _sp_v1_data=2:579348:1673343622:0:4:0:4:0:0:_:-1; _pxde=d373a013cf04a94c19b72652bf9278b6a1bef90f420b1c872025cb0fe7875506:eyJ0aW1lc3RhbXAiOjE2NzM0MzA2NTgwNjgsImZfa2IiOjAsImlwY19pZCI6W119; _ga=GA1.1.994464615.1673423254; _ga_GQ1PBLXZCT=GS1.1.fa363455-73a5-4b41-b0f7-4bbc8ec1c958.2.1.1673430670.0.0.0',
    'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjE5ODI2OTciLCJhcCI6IjE0MDk1Mjc5OCIsImlkIjoiNzRjNmM0YWVmOTFmMjk4NiIsInRyIjoiYWIyYjQ5OTQyNGMyMTYyNDA0MDc1MDMwZTYwZmY0YjAiLCJ0aSI6MTY3MzQzMDY3MDY1NCwidGsiOiIyNTMwMCJ9fQ==',
    'referer': 'https://www.bloomberg.com/search?query=investment%20plan',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'traceparent': '00-ab2b499424c2162404075030e60ff4b0-74c6c4aef91f2986-01',
    'tracestate': '25300@nr=0-1-1982697-140952798-74c6c4aef91f2986----1673430670654',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

# 最大翻页数
MAX_PAGE = 1


class BloombergBlogSpider(scrapy.Spider):
    name = 'bloomberg_blog'
    allowed_domains = ['bloomberg.com']
    start_urls = ['http://bloomberg.com/']
    keyword_list = ["investment plan", "investment planning", "investments advisor"]
    url = "https://www.bloomberg.com/markets2/api/search"
    params_dict = {
        "query": "investment plan",
        "page": "1"
    }
    result_list = []

    custom_settings = {
        'FEED_EXPORT_FIELDS': ["authors", "eyebrow", "headline", "publishedAt", "subtype", "summary", "thumbnail",
                               "type", "url", "search_keyword", "image_id", "image_name", "title_id", "video_name"],
        'FEED_EXPORTERS': {
            'csv': 'investment_blog.pipelines.BloombergCsvItemExporter'},
        'FEEDS': {
            'file:{path}/{name}'.format(path=FILES_STORE, name="Bloomberg_query.csv"): {
                'format': 'csv',
                'encoding': 'utf8'
            }
        },
        'ITEM_PIPELINES': {
            'investment_blog.pipelines.MyFilesPipeline': 300,
        },
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_TIMEOUT': 180,
    }

    def start_requests(self):
        """

        :return:
        """
        for keyword in self.keyword_list:
            # 深拷贝
            params_dict = copy.deepcopy(self.params_dict)
            params_dict["query"] = keyword
            yield scrapy.FormRequest(url=self.url,
                                     formdata=params_dict,
                                     method="get",
                                     headers=SEARCH_HEADER,
                                     dont_filter=True,
                                     meta={"params_dict": params_dict})
            break

    def parse(self, response):
        """

        :param response:
        :return:
        """
        params_dict = response.meta["params_dict"]
        current_page = int(params_dict["page"])
        json_data = json.loads(response.text)
        blog_list = json_data["results"]

        # 如果 results 是 [],一个空的列表list
        if not blog_list:
            return

        # 在blog_dict里添加search_keyword，image_id，title_id等tag
        for blog_dict in blog_list:

            blog_dict["search_keyword"] = params_dict["query"]
            if blog_dict["thumbnail"] != "":
                # 调用 下载图片到s3 的函数
                blog_dict["image_id"] = blog_dict["thumbnail"].split('/')[6]
                blog_dict["image_name"] = "{name}.jpg".format(name=blog_dict["image_id"])

                # 下载图片文件
                files_item = DownloadFilesItem()
                files_item['file_urls'] = blog_dict["thumbnail"]
                files_item['name'] = "bloomberg_jpg/{name}".format(path=FILES_STORE,
                                                                   name=blog_dict["image_name"])
                yield files_item

            blog_dict["title_id"] = blog_dict["url"].split('/')[-1]
            self.result_list.append(blog_dict)

            if blog_dict["subtype"] == "Video":
                yield scrapy.Request(url=blog_dict["url"],
                                     method="get",
                                     headers=SEARCH_HEADER,
                                     dont_filter=True,
                                     callback=self.parse_video_resource_id,
                                     meta={"blog_dict": blog_dict})
            else:
                yield blog_dict

        # 根据 MAX_PAGE 配置参数爬取下一页的内容
        if current_page < MAX_PAGE:
            params_dict["page"] = str(current_page + 1)
            yield scrapy.FormRequest(url=self.url,
                                     formdata=params_dict,
                                     method="get",
                                     headers=SEARCH_HEADER,
                                     dont_filter=True,
                                     callback=self.parse,
                                     meta={"params_dict": params_dict})

    def parse_video_resource_id(self, response):
        """
        解析出网页 resourceId 参数
        :return:
        """
        blog_dict = response.meta["blog_dict"]
        re_rule = r'"resourceId":"(.*?)"'  # 正则规则
        result_list = re.findall(re_rule, response.text)
        if result_list:
            resource_id = result_list[0]
            blog_dict["video_name"] = "{resource_id}.mp4".format(resource_id=resource_id)

            url = "https://www.bloomberg.com/media-manifest/embed?id={resource_id}".format(resource_id=resource_id)

            yield scrapy.Request(url=url,
                                 method="get",
                                 headers=SEARCH_HEADER,
                                 dont_filter=True,
                                 callback=self.parse_download_video,
                                 meta={"blog_dict": blog_dict})

    def parse_download_video(self, response):
        """
        下载视频
        :param response:
        :return:
        """
        blog_dict = response.meta["blog_dict"]
        json_data = json.loads(response.text)
        download_url = json_data['downloadURLs'][VIDEO_SIZE]

        # 下载图片文件
        files_item = DownloadFilesItem()
        files_item['file_urls'] = download_url
        files_item['name'] = "bloomberg_video/{name}".format(name=blog_dict['video_name'])
        yield files_item
        yield blog_dict


# 直接调用scrapy，适合本地开发环境使用
if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl bloomberg_blog".split()
    cmdline.execute(args)
