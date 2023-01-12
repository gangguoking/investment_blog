# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import io
import csv
import scrapy

from itemadapter import ItemAdapter
from scrapy.pipelines.images import FilesPipeline
from scrapy.exporters import BaseItemExporter
from collections.abc import Mapping
from scrapy.utils.python import to_unicode


class InvestmentBlogPipeline:
    def process_item(self, item, spider):
        return item


class MyFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        if 'file_urls' not in item:
            return
        file_url = item['file_urls']
        meta = {'filename': item['name'],
                'download_maxsize': 1073741824,
                'download_warnsize': 1073741824,
                'download_timeout': 1000}
        yield scrapy.Request(url=file_url, meta=meta)

    def file_path(self, request, response=None, info=None):
        return request.meta.get('filename', '')


class BloombergCsvItemExporter(BaseItemExporter):

    def __init__(self, file, include_headers_line=True, join_multivalued=',', errors=None, **kwargs):
        super().__init__(dont_fail=True, **kwargs)
        if not self.encoding:
            self.encoding = 'utf-8'
        self.include_headers_line = include_headers_line
        self.stream = io.TextIOWrapper(
            file,
            line_buffering=False,
            write_through=True,
            encoding=self.encoding,
            newline='',  # Windows needs this https://github.com/scrapy/scrapy/issues/3034
            errors=errors,
        )
        self.csv_writer = csv.writer(self.stream, **self._kwargs)
        self._headers_not_written = True
        self._join_multivalued = join_multivalued

    def serialize_field(self, field, name, value):
        serializer = field.get('serializer', self._join_if_needed)
        return serializer(value)

    def _join_if_needed(self, value):
        if isinstance(value, (list, tuple)):
            try:
                return self._join_multivalued.join(value)
            except TypeError:  # list in value may not contain strings
                pass
        return value

    def export_item(self, item):
        if self._headers_not_written:
            self._headers_not_written = False
            self._write_headers_and_set_fields_to_export(item)

        if 'url' not in item:
            return

        if item['url'] == '' or item['url'] is None:
            return

        fields = self._get_serialized_fields(item, default_value='',
                                             include_empty=True)
        values = list(self._build_row(x for _, x in fields))
        self.csv_writer.writerow(values)

    def _build_row(self, values):
        for s in values:
            try:
                yield to_unicode(s, self.encoding)
            except TypeError:
                yield s

    def _write_headers_and_set_fields_to_export(self, item):
        if self.include_headers_line:
            if not self.fields_to_export:
                # use declared field names, or keys if the item is a dict
                self.fields_to_export = ItemAdapter(item).field_names()
            if isinstance(self.fields_to_export, Mapping):
                fields = self.fields_to_export.values()
            else:
                fields = self.fields_to_export
            row = list(self._build_row(fields))
            self.csv_writer.writerow(row)
