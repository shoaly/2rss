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

    def __init__(self,url,output_file,tpl,encode_code="utf-8",rss_title="unnamed rss",method="get",params={}):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.encode_code = encode_code
        self.url = url
        self.rss_title = rss_title
        self.output_file = output_file
        self.tpl = tpl
        self.params = params
        self.method = method

        # print self.path

    def generate_rss(self,data):
        with open(self.path+"/"+self.tpl,"r") as file:
            rss_tpl = file.read()
            renderer = pystache.Renderer(file_encoding="utf-8",string_encoding="utf-8")
            data['rss_title'] = self.rss_title
            data['source_url'] = self.url
            rss = pystache.render(rss_tpl, data)
            return rss

    def write_to_file(self,content):
        print "write to " + self.output_file
        with open(self.path+'/'+self.output_file, 'w') as xml_file:
            # print repr(content)
            xml_file.write(content.encode("utf-8"))
     
    #返回 unicode         
    def fetch_web_page(self):
        print self.method + ": " + self.url
        if self.method == "get":
            response = requests.get(self.url)
            content = response.content
            return content.decode(self.encode_code)
        else :
            response = requests.post(self.url,self.params)
            content = response.content
            return content.decode(self.encode_code)

    # 获取 item的全文内容, unicode 编码
    def load_item_full_content(self,link):
        response = requests.get(link)
        response = response.content
        response = response.decode(self.encode_code)
        jQuery = pq(response)
        content = jQuery('.mb30')
        # print response.decode("gbk").encode("utf-8")
        content = jQuery(content[0]).html()
        
        # 替换掉乱码 <?xml:namespace prefix = o ns = "urn:schemas-microsoft-com:office:office" /?>
        # content = re.sub(re.compile("<\?xml.*?/\?>"),'',content)

        return content

    def filter_web_page(self):
        page = self.fetch_web_page()
        
        jQuery = pq(page)
        source_item = jQuery(".q-title a")
        items = []
        for key,row in enumerate(source_item):
            title = jQuery(row).text()
            link = jQuery(row).attr("href")
            description = ""
            description = self.load_item_full_content(link)

            items.append({"title":title,"link":link,"description":description})
            print "done: " + link

            # break
        
        return items
        


rss = RSS(encode_code="utf-8",url="http://z.jd.com/search.html",rss_title=u"京东众筹 Rss",output_file="jdzc.xml",tpl="tpl.py",method="post",params={"parentIdHidden":10,"pageNoHidden":1,"sortHidden":"zhtj","wHidden":"关键字查找"})
items = rss.filter_web_page();
# print items
rss_content = rss.generate_rss({"items":items,"lastBuildDate":datetime.today()})
rss.write_to_file(rss_content)








