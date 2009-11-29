from google.appengine.api import urlfetch
import re
from BeautifulSoup import BeautifulSoup

url = "http://djangopeople.net/%s"
latitude = re.compile("var person_latitude = ([\d.-]+);")
longitude = re.compile("var person_longitude = ([\d.-]+);")

class DjangoPeopleError(Exception):
    def __init__(self, code):
        self.code = code

def parse(name):
    result = urlfetch.fetch(url % name)
    if result.status_code != 200:
        raise DjangoPeopleError(result.status_code)
        
    html = result.content
    soup = BeautifulSoup(html)
    data = {"username": name,}
    for key, span in [ 
        ["fn", "given-name"], 
        ["last", "family-name"], 
        ["region", "region"],
        ["aim", "aim"],
        ["yim", "yim"],
        ["gtalk", "gtalk"],
        ["msn", "msn"],
        ["jabber", "jabber"],
        ["django", "django"]
        ]:
        found = soup.find("span", span)
        if found:
            if key == "region":
                data[key] = found.next
                for child in found.findChildren():
                    data[key] += child.next
            else:
                data[key] = found.string
    
    for key, tag, klass, attr in [ 
        ["picture", "img", "main photo", "src"],  
        ["twitter", "a", "twitter", "href"],
        ["delicious", "a", "delicious", "href"],
        ["facebook", "a", "facebook", "href"]
        ]:
        found = soup.find(tag, klass)
        if found:
            data[key] = found.get(attr)
    
    lat = latitude.search(html).groups()
    if lat:
        data["latitude"] = lat[0]

    lng = longitude.search(html).groups()
    if lng:
        data["longitude"] = lng[0]

    data["picture"] = 'http://djangopeople.net' + data["picture"]

    return data
    
if __name__=="__main__":
    from pprint import pprint
    import sys
    pprint(parse(sys.argv[1]))
    