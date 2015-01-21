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
        with open(self.path+'\\rss.xml', 'w') as xml_file:
            # print repr(content)
            xml_file.write(content.encode("utf-8"))

    def fetch_web_page(self):
        print "fetch source http://www.mimivv.com/forumdisplay.php?fid=55"
        url = "http://www.mimivv.com/forumdisplay.php?fid=55"
        response = requests.get(url)
        content = response.content
        return content

    def fetch_content(self,link):
        response = requests.get(link)
        content = response.content
        content = content.decode("gbk")
        # print content.encode("utf-8")
        return content

    def filter_web_page(self):
        page = self.fetch_web_page()
        page = page.decode("gbk").encode("utf-8")
        daily_a_tag = re.findall('<a.*href=.*tid=(\d*).*">(.*最新BT合集)<\/a>',page,re.U);
        
        items = []
        for row in daily_a_tag:
            link = "http://www.mimivv.com/viewthread.php?tid="+row[0]+"&action=printable"
            description = self.fetch_content(link)
            item = {"link":link,"tid":row[0],"title":row[1].decode("utf-8"),"description":description}
            items.append(item)
            print "done: " + link
        return items


rss = RSS()
items = rss.filter_web_page();
rss_content = rss.generate_rss({"rss_title":u"mimiai 本地","items":items,"lastBuildDate":datetime.today()})
rss.write_to_file(rss_content)








