

import re
# from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spider import Spider
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

class DomainSpider(Spider):
  #http://www.domain.com.au/real-estate/buy/vic/melbourne-region/west/altona-meadows/
  DOMAIN = 'www.harcourts.com.au'
  name = 'harcourts'
  allowed_domains = [DOMAIN]
  
  start_urls = [
    'http://www.harcourts.com.au/Property/Residential?pageid=-1&search=&formsearch=true&OriginalTermText=&OriginalLocation=&location=23006&proptype=&min=&max=&minbed=&maxbed=&results=30&page=1'
  ]

  def __init__(self):
    super(DomainSpider, self).__init__()
    self.feed_source = FeedSource.objects.get(id=FeedSourceEnum.HARCOURTS)
    self.import_batch = ImportBatch()
    self.import_batch.save()

    self.counter = 0

  def parse(self, response):
    items = []
    sel = Selector(response)
    results = sel.css('#searchResults').xpath('.//li[@listingid!=\'\']')
    for result in results:
      item = self.parse_item(result)
      if item != None:
        items.append(item)

    request = self.parse_next_page_request(sel);
    if request != None:
      items.append(request);
    return items

  def parse_next_page_request(self, sel):
    url = utils.get_sel_text(sel.css('.pagerNext').css('a::attr(href)'))    
    if url == '':
      return None
    # huh? use own page lmit
    PAGE_LIMIT = 50
    match = re.search('page=(\d+?)', url)
    if (match != None) and (utils.safe_cast(match.group(1), int, 0) > PAGE_LIMIT):
      return None
    request = self.make_requests_from_url('http://' + self.DOMAIN + url)
    request.callback = self.parse
    return request

  def parse_item(self, sel):
    # Extract data
    url = utils.get_sel_text(sel.css('.listingContent').xpath('.//h2/a/@href'))
    address_raw = utils.get_sel_text(sel.css('.listingContent').css('.listAddress').css('h3::text'))
    title_desc = utils.get_sel_text(sel.css('.listingContent').xpath('.//h2/a/text()'))
    short_desc = utils.get_sel_text(sel.css('.listingContent').css('p::text'))
    img_path = utils.get_sel_text(sel.css('.listingImg').xpath('.//a/img/@src'))
    price_raw = utils.get_sel_text(sel.css('.listingContent').css('.propFeatures').css('h3::text'))
    loc_lat = utils.get_sel_text(sel.css('::attr(lat)'))
    loc_long = utils.get_sel_text(sel.css('::attr(lng)'))
    try:
      bedrooms = self.extract_num_of(sel.css('.listingContent').css('.propFeatures').css('.bdrm::text'))
    except:
      bedrooms = 0
    try:
      bathrooms = self.extract_num_of(sel.css('.listingContent').css('.propFeatures').css('.bthrm::text'))
    except:
      bathrooms = 0
    try:
      carpark = self.extract_num_of(sel.css('.listingContent').css('.propFeatures').css('.grge::text'))
    except:
      carpark = 0

    # # huh? this doesnt work
    # agency_img = selector.css('dl.agent').xpath('.//dd/img')
    # agency_name = utils.get_sel_text(agency_img.css('::attr(title)'))
    # agency_img_path = utils.get_sel_text(agency_img.css('::attr(src)'))

    # Populate model
    item = ListingItem()
    item['source'] = self.feed_source
    item['batch'] = self.import_batch
    item['url'] = url
    item['price_raw'] = price_raw
    item['img_path'] = img_path
    item['bedrooms'] = bedrooms
    item['bathrooms'] = bathrooms
    item['carparks'] = carpark
    item['title_desc'] = title_desc 
    item['short_desc'] = short_desc
    item['property_type_raw'] = ''
    item['agency'] = None

    address, suburb, address_raw = self.parse_address(address_raw)
    item['address'] = Address.objects.get_or_create_address(
      address=address, 
      suburb=suburb, 
      state='', 
      postcode='',
      raw=address_raw,
      loc_long=utils.safe_cast(loc_long, float, 0),
      loc_lat=utils.safe_cast(loc_lat,float, 0))

    if Listing.objects.has_duplicate(item):
      # Discard item
      print 'Duplicate detected'
      return None
    else:
      return item

  def parse_address(self, raw):
    try:
      parts = raw.split(',')
      return (parts[1], parts[0], '')
    except:
      return ('', '', raw)

  def extract_num_of(self, sel):
    text = utils.get_sel_text(sel)
    match = re.search('(\d+?)<img')#'page=(\d+?)', url)
    if match != None:
      return utils.safe_cast(match.group(1), int, 0)
    return 0
