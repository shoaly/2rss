#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import pystache
import requests
import re
import time  
import os
from datetime import *  

 
# print pystache.render('Hi {{person}}!', {'person': 'Mom'})

class RSS:

    def __init__(self,url,output_file,tpl,encode_code="utf-8",rss_title="unnamed rss"):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.encode_code = encode_code
        self.url = url
        self.rss_title = rss_title
        self.output_file = output_file
        self.tpl = tpl

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

    def fetch_web_page(self):
        print "fetch " + self.url
        response = requests.get(self.url)
        content = response.content
        return content.decode(self.encode_code)

    def load_item_full_content(self,link):
        response = requests.get(link)
        content = response.content
        content = content.decode(self.encode_code)
        return content

    def filter_web_page(self):
        page = self.fetch_web_page()
        page = page.encode("utf-8")
        daily_a_tag = re.findall('<a.*href=.*tid=(\d*).*">(.*最新BT合集)<\/a>',page,re.U);
        
        items = []
        for row in daily_a_tag:
            link = "http://www.mimivv.com/viewthread.php?tid="+row[0]+"&action=printable"
            description = self.load_item_full_content(link)
            item = {"link":link,"title":row[1].decode("utf-8"),"description":description}
            items.append(item)
            print "done: " + link
        return items


rss = RSS(encode_code="gbk",url="http://www.mimivv.com/forumdisplay.php?fid=55",rss_title="Mimi Rss",output_file="mimi.xml",tpl="tpl.py")
items = rss.filter_web_page();
rss_content = rss.generate_rss({"rss_title":u"mimiai 本地","items":items,"lastBuildDate":datetime.today()})
rss.write_to_file(rss_content)








