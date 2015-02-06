#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import urllib2
import pystache
import requests
import re
import os
from datetime import *
import time  
from pyquery import PyQuery as pq
import Queue

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
## print pystache.render('Hi {{person}}!', {'person': 'Mom'})

class RSS:

    def __init__(self,url,output_file,tpl,encode_code="utf-8",rss_title="unnamed rss"):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.encode_code = encode_code
        self.url = url
        self.lock = threading.Lock() 
        self.rss_title = rss_title
        self.output_file = output_file
        self.tpl = tpl

        self.workers = [] # 储存所有线程, 由于线程里面的run 是一个死循环, 所以最后当queue处理完毕的时候, 需要关闭所有的子线程

        # print self.path

    def generate_rss(self,data):
        with open(self.path+"/"+self.tpl,"r") as file:

            items = []
            for key in data['items']:
                items.append(data['items'][key])
                print data['items'][key]
            data['items'] = items

            rss_tpl = file.read()
            renderer = pystache.Renderer(file_encoding="utf-8",string_encoding="utf-8")
            data['rss_title'] = self.rss_title
            data['source_url'] = self.url
            try:
                rss = pystache.render(rss_tpl, data)
            except:
                print "error"
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

   

    # 获取 item的全文内容, unicode 编码
    def load_item_full_content(self,items,threads_num = 5):
        # print "start 5 threads to fullfil task"
        
        queue = Queue.Queue()
        for key in items:
            queue.put(items[key])
        
        for i in range(threads_num):
            # print "new worker %s" % i
            worker = FetchContent(queue = queue, items = items,lock = self.lock, encode_code = self.encode_code)
            worker.setDaemon(True) # 这个很重要, 让主线程完成之后 也关闭这些 worker线程, 否则程序不会结束
            worker.start()
            self.workers.append(worker)
        queue.join()
        return items


    # 找出页面上需要的链接
    def filter_links(self):
        page = self.fetch_web_page()
        
        jQuery = pq(page)

        source_item = jQuery(".channel-item h3 a")
        # print source_item
        items = {}
        for key,row in enumerate(source_item):
            title = jQuery(row).text()
            link = jQuery(row).attr("href")
            link = str(link).strip() # 去掉首尾空格
            
            items[link] = {"title":title,"link":link,"description":""}

        
            
            # print "done: " + link
        return items
        

class FetchContent(threading.Thread):
    # 传入 items数组 和 需要处理的 item的 index下标
    def __init__(self,queue,items,lock,encode_code = "utf-8"):
        threading.Thread.__init__(self)
        print "%s init" % self.getName()
        self.queue = queue
        self.items = items
        self.lock = lock
        self.encode_code = encode_code
        self.running_flag = True # 留一个flag 主线程可以 通过这个flag 退出 run 循环
    
     

    def run(self):
        while self.running_flag:
            item = self.queue.get()
            response = requests.get(item['link'])
            response = response.content
            print "%s is fetching url : %s , size: %s" % (self.getName(),item['link'], len(response))
            response = response.decode(self.encode_code)
            jQuery = pq(response)
            content = jQuery('.topic-doc')

            try:
                content = jQuery(content[0]).html()
                # title = jQuery(".title").text() 
                # self.items[item['link']]['title'] = title
                self.items[item['link']]['description'] = content
            except:
                self.lock.acquire()
                print "remove unhealthy item, url : %s" % item['link']
                self.items.pop(item['link'],"default")
                self.lock.release()
            

            self.queue.task_done()
            
start = time.time()
rss = RSS(encode_code="utf-8",url="http://www.douban.com/group/explore",rss_title=u"豆瓣话题精选",output_file="douban_huati.xml",tpl="tpl.py")
items = rss.filter_links();
# print items
items = rss.load_item_full_content(items)

rss_content = rss.generate_rss({"items":items,"lastBuildDate":datetime.today()})
rss.write_to_file(rss_content)


print "Elapsed time: %s" % (time.time()-start)







