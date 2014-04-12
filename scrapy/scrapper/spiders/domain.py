

import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapper import settings, utils
from scrapper.items import ListingItem
from rescrap.models import FeedSourceEnum, FeedSource, ImportBatch, Address, Agency, Listing

def add_url_attr(url):
  sort_arg = 'sort=date-asc' if settings.DATE_ORDER_NEWEST else 'sort=date-desc'
  res = url #+ '?' + sort_arg
  #print res
  return res

class DomainSpider(CrawlSpider):
  #http://www.domain.com.au/real-estate/buy/vic/melbourne-region/west/altona-meadows/
  DOMAIN = 'www.domain.com.au'
  name = 'domain'
  allowed_domains = [DOMAIN]
  
  start_urls = [
    'http://www.domain.com.au/real-estate/buy/vic/'
  ]


  rules = (
    Rule(SgmlLinkExtractor(allow=('/real-estate/buy/vic/'), process_value=add_url_attr), callback='parse_suburb'),
  )

  def __init__(self):
    super(DomainSpider, self).__init__()
    self.feed_source = FeedSource.objects.get(id=FeedSourceEnum.DOMAIN)
    self.import_batch = ImportBatch()
    self.import_batch.save()

    self.counter = 0


  def parse_suburb(self, response):
    print response.url
    
    if response.url == 'http://www.domain.com.au/real-estate/buy/vic/':
      print 'Ignoring start page'
      return None

    # if self.counter > 4:
    #   return None
       
    # self.counter += 1

    items = []
    sel = Selector(response)
    results = sel.css('.s-listing')
    for result in results:
      item = self.parse_item(result)
      if item != None:
        items.append(item)

    request = self.parse_next_page_request(sel);
    if request != None:
      items.append(request);
    return items

  def parse_next_page_request(self, selector):
    url = utils.get_sel_text(selector.css('.next').css('a::attr(href)'))    
    if url == '':
      return None
    if settings.PAGE_LIMIT != None:
      match = re.search('page=(\d+?)', url)
      if (match != None) and (utils.safe_cast(match.group(1), int, 0) > settings.PAGE_LIMIT):
        return None
    request = self.make_requests_from_url('http://' + self.DOMAIN + url)
    request.callback = self.parse_suburb
    return request

  def parse_item(self, selector):
    # Extract data
    url = utils.get_sel_text(selector.css('.feat-wrap').css('a.detailsLink::attr(href)'))
    address_raw = utils.get_sel_text(selector.css('.feat-wrap').css('a.detailsLink::text'))
    desc_node = selector.css('.description')
    price_raw = utils.get_sel_text(desc_node.css('h4::text'))
    title_desc = utils.get_sel_text(desc_node.css('h5::text'))
    short_desc = utils.get_sel_text(desc_node.css('p::text'))
    property_type = utils.get_sel_text(selector.css('dd.propertytype::text'))
    img_path = utils.get_sel_text(selector.css('.photo').css('img::attr(src)'))
    bedrooms = utils.get_sel_text(selector.css('dd.bedrooms::text'))
    bathrooms = utils.get_sel_text(selector.css('dd.bathrooms::text'))
    carspaces = utils.get_sel_text(selector.css('dd.carspaces::text'))

    agency_img = selector.css('dl.agent').xpath('.//dd/img')
    agency_name = utils.get_sel_text(agency_img.css('::attr(title)'))
    agency_img_path = utils.get_sel_text(agency_img.css('::attr(src)'))

    # Populate model
    item = ListingItem()
    item['source'] = self.feed_source
    item['batch'] = self.import_batch
    item['url'] = url
    item['price_raw'] = price_raw
    item['img_path'] = img_path
    item['bedrooms'] = utils.safe_cast(bedrooms, int)
    item['bathrooms'] = utils.safe_cast(bathrooms, int)
    item['carparks'] = utils.safe_cast(carspaces, int)
    item['title_desc'] = title_desc 
    item['short_desc'] = short_desc
    item['property_type_raw'] = property_type

    if agency_name != '':
      item['agency'] = Agency.objects.get_or_create(name=agency_name.lower().strip())[0]
      item['agency'].img_path = agency_img_path
    else:
      item['agency'] = None

    address, suburb, address_raw = self.parse_address(address_raw)
    item['address'] = Address.objects.get_or_create_address(
      address=address, 
      suburb=suburb, 
      state='', 
      postcode='',
      raw=address_raw)

    if Listing.objects.has_duplicate(item):
      # Discard item
      print 'Duplicate detected'
      return None
    else:
      return item

  def parse_address(self, raw):
    try:
      parts = raw.split(',')
      return (parts[0], parts[1], '')
    except ValueError:
      return ('', '', raw)

  # def parse_suburb_xml_feed(self, response):
  #   items = []
  #   selector = Selector(response)
  #   results = selector.xpath('//img')
  #   item = self.parse_item(result)
  #   if item != None:
  #     items.append(item)
  #   return items

  # def parse_xml_feed item(self, selector):
  #   desc_node = selector.xpath('.//description')
  #   url = utils.get_sel_text(desc_node.xpath('.//a/@href'))
  #   img_path = utils.get_sel_text(desc_node.xpath('.//img/@src'))
  #   title_desc = utils.get_sel_text(desc_node.xpath('.//p/B'))
  #   short_desc = utils.get_sel_text(desc_node.xpath('.//p/')).split('<br>')[1]
  #   pub_date = utils.safe_parse_date_utc(utils.get_sel_text(selector.xpath('.//pubDateParsed/text')))
