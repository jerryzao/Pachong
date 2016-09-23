# coding=utf-8
import requests
import urllib
from bs4 import BeautifulSoup as BS
import time
import MySQLdb


class qxb(object):
    def __init__(self):
        pass

    def create_cursor(self):
        self.conn = MySQLdb.connect(host='172.16.0.20',port=3306,user='zhangxiaogang',passwd='gangxiaozhang',db='SpotCheck',charset='utf8')
        self.cursor=self.conn.cursor()

    def insert_into_database(self,sql):
#         print sql
        self.cursor.execute(sql)
        self.conn.commit()


    def get_web(self,page):
        self.create_cursor()
        baseUrl = 'http://www.baidu.com/s'
        # page = 2 #第几页
        word = '统一社会信用代码 怎么样-启信宝'  #搜索关键词
        data = {'wd':word,'pn':str(page-1)+'0','op':'word','ie':'utf-8','usm':'1','rsv_idx':'1'}
        data = urllib.urlencode(data)
        url = baseUrl+'?'+data
        print "url", url  # here OK
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Connection':'keep-alive',
            'Host':'www.baidu.com'}
        # print url

        r = requests.get(url)
        # r = requests.get(url,headers=headers)
        print r.encoding
        soup = BS(r.text,'html5lib')
        # print 'soup', soup
        content=soup.find(id='content_left')
        # print 'content',content

        for element in content.find_all(class_='c-container'):

            n = element.find_all(class_='c-abstract')[0]
            bbb = n.get_text()
            # print 'bbb', bbb
            xydm = bbb.split(u'统一社会信用代码:')[1].split(u'组织机构代码:')[0]
            # print 'xydm',xydm #Here OK
            zzjgdm = bbb.split(u'组织机构代码:')[1].split(u' 注册号:')[0]
            # print 'zzjgdm', zzjgdm #Here OK
            zch = bbb.split(u'注册号:')[1][1:16]
            # print 'zch', zch #Here Ok
            gsm = bbb.split(u'怎么样?启信宝')[0]
            if u'想知道' in gsm:
                gsm = gsm.split(u'想知道')[1]
                # print 'gsm', gsm  #Here OK
            elif u'想了解' in gsm:
                gsm = gsm.split(u'想了解')[1]
                # print 'gsm', gsm  #Here OK
            else:
                gsm = ''
            updatetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

            sql = "insert into qxb values('%s','%s','%s','%s','%s')" %(gsm, xydm, zzjgdm, zch, updatetime)

            self.insert_into_database(sql)
            print page, '**', sql




if __name__ == '__main__':
    go = qxb()
    for i in range(40, 76):
        go.get_web(i)
