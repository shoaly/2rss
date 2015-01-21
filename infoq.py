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

    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        # print self.path

    def generate_rss(self,data):
        with open(self.path+"\\tpl.py","r") as file:
            rss_tpl = file.read()
            renderer = pystache.Renderer(file_encoding="utf-8",string_encoding="utf-8")
            rss = pystache.render(rss_tpl, data)
            return rss

    def write_to_file(self,content):
        print "write to rss.xml"
        with open(self.path+'\\infoq_rss.xml', 'w') as xml_file:
            # print repr(content)
            xml_file.write(content.encode("utf-8"))

    def fetch_web_page(self):
        url = "http://www.infoq.com/cn/rss/rss.action?token=4POLcv0YSybIGMOrTRWssL4E6ho53LHv"
        print "fetch " + url
        response = requests.get(url)
        content = response.content
        return content

    def fetch_item_content(self,link):
        response = requests.get(link)
        response = response.content
        response = response.decode("utf-8")

        jQuery = pq(response)
    

        jQuery("body").append('<style>#header{display:none} #topInfo{display:none} #rightbarcontentbox{display:none} #footer{display:none} #postFormDeck{display:none}</style>')
        content = "<html>"+jQuery("html").html() + "</html>"
        content = content.replace("&#13;"," ");
        # print repr(response)
        return content

    def filter_web_page(self):
        page = self.fetch_web_page()
        # page = page.decode("utf-8").encode("utf-8")
        page = page.decode("utf-8")

        row_link = re.findall('<item>.*?<link>(.*?)</link>.*?<\/item>',page,re.S) # S DOT ALL
        row_title = re.findall('<item>.*?<title>(.*?)</title>.*?<\/item>',page,re.S) # S DOT ALL

        items = []

        for index,link in enumerate(row_link):
            description = self.fetch_item_content(link)
            item = {"link":link,"title":row_title[index],"description":description}
            items.append(item)
            print "done: " + link
        return items


rss = RSS()
items = rss.filter_web_page();
# print items
rss_content = rss.generate_rss({"rss_title":"infoQ","items":items,"lastBuildDate":datetime.today()})
rss.write_to_file(rss_content)








