#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import pystache
import requests
import re
import time  
import os
from datetime import *
from pyquery import PyQuery as pq
from lxml import etree


 
# print pystache.render('Hi {{person}}!', {'person': 'Mom'})

class RSS:

    def __init__(self,url,output_file,tpl,encode_code="utf-8",rss_title="unnamed rss"):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.encode_code = encode_code
        self.url = url
        self.rss_title = rss_title
        self.output_file = output_file
        self.tpl = tpl

        # print self.path

    def generate_rss(self,data):
        with open(self.path+"/"+self.tpl,"r") as file:
            rss_tpl = file.read()
            renderer = pystache.Renderer(file_encoding="utf-8",string_encoding="utf-8")
            rss = pystache.render(rss_tpl, data)
            return rss

    def write_to_file(self,content):
        print "write to " + self.output_file
        with open(self.path+'/'+self.output_file, 'w') as xml_file:
            # print repr(content)
            xml_file.write(content.encode("utf-8"))
     
    #返回 unicode         
    def fetch_web_page(self):
        
        print "fetch " + self.url
        response = requests.get(self.url)
        content = response.content
        return content.decode(self.encode_code)

    # 获取 item的全文内容, unicode
    def load_item_full_content(self,link):
        response = requests.get(link)
        response = response.content
        response = response.decode(self.encode_code)
        jQuery = pq(response)
        content = jQuery('table[width="680"]')
        # print response.decode("gbk").encode("utf-8")
        content = jQuery(content[1]).html()
        
        # 替换掉乱码 <?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /?>
        content = re.sub(re.compile("<\?xml.*?/\?>"),'',content)

        return content
        # return content.decode(self.encode_code);

    def filter_web_page(self):
        page = self.fetch_web_page()
        
        jQuery = pq(page)

        rss_row1 = jQuery("table[background='images/index_25.jpg'] a")
        items = []
        for key,row in enumerate(rss_row1):
            title = jQuery(row).html()
            link =  "http://www.tcsisu.com"+jQuery(row).attr("href")
            description = self.load_item_full_content(link);
            items.append({"title":title,"link":link,"description":description})
            print "done: " + link
            # break

        
        return items
        


rss = RSS(encode_code="gbk",url="http://www.tcsisu.com/",rss_title="南方翻译Rss",output_file="tcsisu.xml",tpl="tpl.py")
items = rss.filter_web_page();
# print items
rss_content = rss.generate_rss({"items":items,"lastBuildDate":datetime.today()})
rss.write_to_file(rss_content)








