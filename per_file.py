import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def unit_file(url):
    if url == "":
        url = 'https://archive.org/download/Maximum_PC_April_2005'
    html = urllib.request.Request(url, headers = hdr)                     # Header is added so that this program behaves like a Browser
    html_read = urllib.request.urlopen(html, context = ctx).read()        # reads all HTML data, but in a single line
    soup = BeautifulSoup(html_read, 'html.parser')

    #soup_str = soup.prettify()                                            # Prettify the HTML, but it becomes String
    #print(soup_str)

    dict = {}

    tags = soup.find_all("tr")                    # Extracts tags with tag div Class = tile-img       
    count = 0

    for tag in tags:
        count += 1
        if count == 0:
            continue
        else:
            file_name = tag.td.a.get('href')
            if (re.findall('_text[/.].+',file_name)):
                continue
            else:
                file_format = re.findall("[/.].+",file_name)[0]
                size = tag.find_all("td")[2::3][0].text

                if size != "":
                    dict[file_format] = [file_name,size]
    
    try:
        a = (dict['.djvu'])
    except:
        dict['.djvu'] = ["",""]

    try:
        a = (dict['.gz'])
    except:
        dict['.gz'] = ["",""]
    
    del a

    return dict


# local_output = unit_file("")
# print(local_output)