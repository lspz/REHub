# TODO: scrap property type

import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapper import settings, utils
from scrapper.items import ListingItem
from rescrap.models import FeedSourceEnum, FeedSource, ImportBatch, Address, Agency, Listing

def add_url_attr(url):
  sort_arg = 'activeSort=list-date' if settings.DATE_ORDER_NEWEST else 'activeSort=list-date-asc'
  res = url + '?' + sort_arg + '&includeSurrounding=false'
  #print res
  return res

class REACOMAUSpider(CrawlSpider):
  #http://www.realestate.com.au/buy/in-apollo+bay%2c+vic+3233/list-1
  DOMAIN = 'www.realestate.com.au'
  name = 'reacomau'
  allowed_domains = [DOMAIN]
  
  start_urls = [
    #'http://www.realestate.com.au/buy/in-north+melbourne%2c+vic+3051/list-1',
    'http://www.rs.realestate.com.au/sitemap/victoria'
  ]

  rules = (
    Rule(SgmlLinkExtractor(allow=('/buy/in-'), process_value=add_url_attr), callback='parse_suburb'),
  )

  def __init__(self):
    super(REACOMAUSpider, self).__init__()
    self.feed_source = FeedSource.objects.get(id=FeedSourceEnum.RECOMAU)
    self.import_batch = ImportBatch()
    self.import_batch.save()

  def parse_suburb(self, response):
    items = []
    sel = Selector(response)
    results = sel.css('#searchResultsTbl').css('.resultBody')
    for result in results:
      item = self.parse_item(result)
      if item != None:
        items.append(item)

    request = self.parse_next_page_request(sel);
    if request != None:
      items.append(request);
    return items

  def parse_next_page_request(self, selector):
    url = utils.get_sel_text(selector.css('.nextLink').css('a[rel*=newSearchPage]::attr(href)'))    
    if url == '':
      return None
    if settings.PAGE_LIMIT != None:
      match = re.search('list-(\d+?)', url)
      if (match != None) and (utils.safe_cast(match.group(1), int, 0) > settings.PAGE_LIMIT):
        return None
    request = self.make_requests_from_url('http://' + self.DOMAIN + url)
    request.callback = self.parse_suburb
    return request

  def parse_item(self, selector):
    # This one is truncated 
    #address = result.css('.vcard').css('.name').extract()

    # Extract data
    price_raw = utils.get_sel_text(selector.css('.price').css('span::text'))
    raw_address = utils.get_sel_text(selector.css('.photoviewer').css('img::attr(alt)'))
    img_path = utils.get_sel_text(selector.css('.photoviewer').css('img::attr(src)'))
    url = utils.get_sel_text(selector.css('.vcard').css('a::attr(href)'))

    info = selector.css('.listingInfo')
    
    property_type = utils.get_sel_text(info.css('.propertyType::text')) 
    bedrooms = utils.get_sel_text(info.xpath('.//img[@alt="Bedrooms"]/..//span/text()'))
    bathrooms = utils.get_sel_text(info.xpath('.//img[@alt="Bathrooms"]/..//span/text()'))
    carparks = utils.get_sel_text(info.xpath('.//img[@alt="Car Spaces"]/..//span/text()'))
    title_desc = utils.get_sel_text(info.css('.title::text'))
    short_desc = utils.get_sel_text(info.css('.description::text')) 

    elite_wrapper = selector.css('.enhancedWrapper') 
    if len(elite_wrapper.extract()) > 0:
      agency_img = elite_wrapper.css('img.logo')
    else:
      agency_img = info.css('img.logo')
    
    agency_name = utils.get_sel_text(agency_img.css('::attr(alt)'))
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
    item['carparks'] = utils.safe_cast(carparks, int)
    item['title_desc'] = title_desc 
    item['short_desc'] = short_desc
    item['property_type_raw'] = property_type

    agency_name = self.parse_agent_name(agency_name)
    if agency_name != '':
      item['agency'] = Agency.objects.get_or_create(name=agency_name)[0]
      item['agency'].img_path = agency_img_path
    else:
      item['agency'] = None

    address, suburb, state, postcode, raw_address = self.parse_address(raw_address)
    item['address'] = Address.objects.get_or_create_address(
      address=address, 
      suburb=suburb, 
      state=state, 
      postcode=postcode,
      raw=raw_address)

    if Listing.objects.has_duplicate(item):
      # Discard item
      print 'Duplicate detected'
      return None
    else:
      return item

  def parse_agent_name(self, raw_name):
    tokens = raw_name.split('-')
    return tokens[0].strip().lower()

  def parse_address(self, raw_address):
    try:
      address, suburb, state = raw_address.split(',', 3) 
      state, postcode = state.strip().split(' ', 2)
      return (address.strip(), suburb.strip(), state.strip(), postcode.strip(), '')
    except ValueError:
      return ('', '', '', '', raw_address) 








