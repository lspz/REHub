# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapper import settings
from rescrap.models import Listing

class DataSavePipeline(object):
  def open_spider(self, spider):
    if settings.DELETE_ON_CRAWL:
      Listing.objects.all().delete()

  def process_item(self, item, spider):
    item.save()
    return item

  # def close_spider(spider):
  #    pass
