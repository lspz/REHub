import datetime

def safe_cast(val, to_type, default=None):
  try:
    return to_type(val)
  except ValueError:
    return default

def safe_parse_date_utc(date_string):
  try:
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
  except ValueError:
    return None

def get_sel_text(selector_list):
  # huh? add logging
  str_list = selector_list.extract()
  if len(str_list) > 0:
    return str_list[0]
  else:
    return ''