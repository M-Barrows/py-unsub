import base64
import re

def find_unsub_urls(text:str):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)
    links = [x[0] for x in url if "unsub" in x[0]] 
    return links[0] if len(links) > 0 else 'None'

def get_content(msg, path:list):
    location = path.pop(0)
    if not msg.get(location):
        return None
    if len(path) == 0:
        return msg.get(location)
    else:
        return get_content(msg.get(location),path)
    
def get_header(msg,header_name:str) -> str:
    headers = get_content(msg, ['payload','headers'])
    if headers:
        val = [header.get('value') for header in headers if header.get('name') == header_name]
    if val: 
        return val[0]
    else: 
        return None

def parse_link(link:str):
    return link.replace('"','')

def remove_mailto_links(links:list):
    filtered_links = list(filter(lambda x: any(substring not in x for substring in ['mailto:']), links))
    if len(filtered_links)>0:
        return filtered_links[0]
    return 'None'

def get_unsub_links(message_obj) -> str:
    if get_header(message_obj,"List-Unsubscribe"):
        unsub = parse_link(remove_mailto_links(get_header(message_obj,"List-Unsubscribe").split(', ')))
    elif get_content(message_obj, ['body','data']) :
        body_str = base64.urlsafe_b64decode(message_obj.get("body").get("data").encode("ASCII")).decode("utf-8")
        unsub = find_unsub_urls(body_str)
    elif get_content(message_obj, ['payload','body','data']):
        body_str = base64.urlsafe_b64decode(message_obj.get("payload").get("body").get('data').encode("ASCII")).decode("utf-8")
        unsub = find_unsub_urls(body_str)
    elif get_content(get_content(message_obj, ['payload','parts'])[0],['body','data']):
        body_str = base64.urlsafe_b64decode(message_obj.get("payload").get("parts")[0].get("body").get('data').encode("ASCII")).decode("utf-8")
        unsub = find_unsub_urls(body_str)
    else: 
        unsub = "None"
    return unsub
