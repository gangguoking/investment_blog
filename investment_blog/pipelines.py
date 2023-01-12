# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import FilesPipeline


class InvestmentBlogPipeline:
    def process_item(self, item, spider):
        return item


class MyFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if 'file_urls' not in item:
            return
        file_url = item['file_urls']
        meta = {'filename': item['name']}
        yield scrapy.Request(url=file_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')
