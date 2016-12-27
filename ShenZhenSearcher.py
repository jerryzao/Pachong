#coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
import time
import sys
import xlrd
import MySQLdb

class ShenZhenSearcher(object):
    def __init__(self):
        self.failed_times = 0

    def create_cursor(self):
        self.conn = MySQLdb.connect(host='172.16.0.76',port=3306,user='guanhuaixuan',passwd='123QWEasd',db='qianshui',charset='utf8')
        self.cursor=self.conn.cursor()

    def insert_into_database(self,sql):
        # print sql
        self.cursor.execute(sql)
        self.conn.commit()

    def get_xls(self):
        xls_add_list = []
        url = 'http://www.szgs.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=1&endrecord=40&perpage=20'
        headers={'Accept':'application/xml, text/xml, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Content-Length':'136',
                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie':'JSESSIONID=8T26YJMG4dLR6VGb6blchZFlhrfhW71wlBBNGpBL6hwhcHyLhJVT!-2088070185',
                'Host':'www.szgs.gov.cn',
                'Referer':'http://www.szgs.gov.cn/col/col43/index.html',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'X-Requested-With':'XMLHttpRequest'}

        payload={'col':'1',
                'appid':'1',
                 'webid':'1',
                 'path':'/',
                 'columnid':'43',
                 'sourceContentType':'3',
                 'unitid':'2137',
                 'webname':u'深圳国税',
                 'permissiontype':'0'}

        headers2={'Host': 'www.szgs.gov.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Cookie': 'JSESSIONID=37y2YJZCzJthjzPgRvyvbPjTyDRNLK9CKtm2Wy1nF4FDPGkZV1ML!-2088070185',
                'Connection': 'keep-alive',
                'If-Modified-Since': 'Wed, 07 Sep 2016 07:41:17 GMT',
                'If-None-Match': '"8a0df0-4118-53be609d4a140"',
                'Cache-Control': 'max-age=0'}

        # r = requests.session().get(url=url,headers=headers)
        r = requests.post(url=url, headers=headers, data=payload)
        # print r
        soup = BeautifulSoup(r.text,'html5lib')
        # print soup
        n = soup.find_all('a')
        # print n
        for element in n:
            m = element.get('href')
            # print m
            url_2 = 'http://www.szgs.gov.cn' + m
            print '*****', url_2
            r2 = requests.get(url=url_2, headers=headers2)
            # print r2
            soup2 = BeautifulSoup(r2.content, 'xml')
            # print soup2
            try:
                mmmm = soup2.find(id='zoom')
                # print mmmm
                s = mmmm.find_all('a')
                # print '***&&&**&*&*&', len(s), s
                for d in range(0, len(s)):
                    dd = s[d].get('href')
                    # print dd
                    # /module/download/downfile.jsp?classid=0&filename=1511231021346667307.xlsx
                    try:
                        dd_1 = dd.split('=' ,2)[0]
                        # print 'dd_1', dd_1
                        dd_2 = dd.split('=', 2)[2]
                        # print 'dd_2', dd_2
                        xls_add = 'http://www.szgs.gov.cn' + dd_1 + '=0&filename=' + dd_2
                        # print '####', xls_add
                        xls_add_list.append(xls_add)
                    except:
                        pass
            except:
                pass

        print len(xls_add_list), '&&&',  xls_add_list
        return xls_add_list

    def save_xls(self,folder,xls_add_list):
        headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                }
        for each in xls_add_list:
            filename = each.split('filename=')[1]
            with open(filename, 'wb') as f:
                xls = requests.get(url=each, headers=headers)
                f.write(xls.content)

    def download_XLS(folder):
        folder = 'ShenZhen_XLS'
        try:
            os.mkdir(folder)
            os.chdir(folder)
        except:
            os.chdir(folder)

        xls_add_list = ShenZhenSearcher().get_xls()
        ShenZhenSearcher().save_xls(folder, xls_add_list)
        print u'更新完成*********'

    def get_details(self):
        xls_add_list = ShenZhenSearcher().get_xls()
        self.create_cursor()
        update_time = time.strftime("%Y-%m-%d")
        for each in xls_add_list:
            filename = each.split('filename=')[1]
            xls_path = sys.path[0]+ r'\ShenZhen_XLS'+ '\\'+ filename
            print 'xls_path:', xls_path
            try:
                d = xlrd.open_workbook(xls_path)
                table = d.sheets()[0]
                nrows = table.nrows
                ncols = table.ncols
                print 'nrows = ', nrows, '#####', 'ncols = ', ncols

                for rn in range(0, nrows):
                    row_val = table.row_values(rn) #每一行
                    a = row_val[0].strip()
                    # print a
                    if a == u'序号':
                        b = rn
                        # print u'序号出现的行数', b
                        break

                    elif a == u'纳税人识别号':
                        b = rn
                        # print u'序号出现的行数', b
                        break
                    else:
                        pass

                for rn_2 in range(b+1, nrows):
                    row_val = table.row_values(rn_2)
                    if ncols == 9:
                        cc = row_val[2]
                        c = cc[0]
                        # print u'c是否为所有为数字', c.isdigit(), c
                        if c.isdigit() is True:
                            enterprise = row_val[1].strip()
                            # print 'enterprise = ', enterprise

                            try:
                                number = int(row_val[2])
                            except:
                                number = row_val[2]
                            # print 'number = ', number

                        else:
                            try:
                                number = int(row_val[1])
                            except:
                                number = row_val[1]
                            # print 'number = ', number

                            enterprise = row_val[2].strip()
                            # print 'enterprise = ', enterprise

                        name = row_val[3].strip()
                        # print 'name = ', name

                        try:
                            id = int(row_val[4])
                        except:
                            id = row_val[4]
                        # print 'id = ', id

                        place = row_val[5].strip()
                        # print 'place = ', place

                        kind = row_val[6].strip()
                        # print 'kind = ', kind

                        money = row_val[7]
                        # print 'money = ', money

                        last_money = row_val[8]
                        # print 'last_money = ', last_money

                        sql = "insert into shen_zhen (enterprise, number, name, id, place, kind, money,last_money,update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, number, name, id, place, kind, money,last_money,update_time, filename)
                        try:
                            self.insert_into_database(sql)
                            print 'sql', sql
                            print u'*****************此条写入成功!!!*****************'

                        except Exception, e:
                            print e
                            print u'!!!!!!!!!!!!!!!此条已存在!!!!!!!!!!!'
                            self.failed_times += 1
                            print u'累计失败%s' % self.failed_times




                    elif ncols == 8:
                        cc = row_val[1]
                        c = cc[0]
                        if c.isdigit() is True:
                            try:
                                number = int(row_val[1])
                            except:
                                number = row_val[1]
                            # print 'number = ', number

                            enterprise = row_val[2]
                            # print 'enterprise = ', enterprise
                        else:
                            try:
                                number = int(row_val[2])
                            except:
                                number = row_val[2]
                            # print 'number = ', number

                            enterprise = row_val[1]


                        name = row_val[3]
                        # print 'name = ', name

                        try:
                            id = int(row_val[4])
                        except:
                            id = row_val[4]
                        # print 'id = ', id

                        kind = row_val[5]
                        # print 'kind = ', kind

                        money = row_val[6]
                        # print 'money = ', money

                        last_money = row_val[7]
                        # print 'last_money = ', last_money

                        sql = "insert into shen_zhen (enterprise, number, name, id, kind, money, last_money, update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, number, name, id, kind, money, last_money, update_time, filename)
                        try:
                            self.insert_into_database(sql)
                            print 'sql', sql
                            print u'*****************此条写入成功!!!*****************'

                        except Exception, e:
                            print e
                            print u'!!!!!!!!!!!!!!!此条已存在!!!!!!!!!!!'
                            self.failed_times += 1
                            print u'累计失败%s' % self.failed_times




                    elif ncols == 7:
                        cc = row_val[2]
                        c = cc[0]
                        if c.isdigit() is True:
                            enterprise = row_val[1]
                            # print 'enterprise = ', enterprise

                            try:
                                number = int(row_val[2])
                            except:
                                number = row_val[2]
                            # print 'number = ', number
                        else:
                            enterprise = row_val[2]
                            # print 'enterprise = ', enterprise

                            try:
                                number = int(row_val[1])
                            except:
                                number = row_val[1]
                            # print 'number = ', number

                        place = row_val[3].strip()
                        # print 'place = ', place

                        kind = row_val[4]
                        # print 'kind = ', kind

                        money = row_val[5]
                        # print 'money = ', money

                        last_money = row_val[6]
                        # print 'last_money = ', last_money


                        sql = "insert into shen_zhen (enterprise, number, place, kind, money, last_money, update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, number, place, kind, money, last_money, update_time, filename)
                        try:
                            self.insert_into_database(sql)
                            print 'sql', sql
                            print u'*****************此条写入成功!!!*****************'

                        except Exception, e:
                            print e
                            print u'!!!!!!!!!!!!!!!此条已存在!!!!!!!!!!!'
                            self.failed_times += 1
                            print u'累计失败%s' % self.failed_times




                    elif ncols == 13:
                        cc = row_val[0]
                        c = cc[0]
                        if c.isdigit() is True:
                            try:
                                number = int(row_val[0])
                            except:
                                number = row_val[0]
                            # print 'number = ', number

                            enterprise = row_val[1]
                            # print 'enterprise = ', enterprise
                        else:
                            try:
                                number = int(row_val[1])
                            except:
                                number = row_val[1]
                            # print 'number = ', number

                            enterprise = row_val[0]
                            # print 'enterprise = ', enterprise

                        name = row_val[2].strip()
                        # print 'name = ', name

                        try:
                            id = int(row_val[4])
                        except:
                            id = row_val[4]
                        # print 'id = ', id

                        place = row_val[5].strip()
                        # print 'place = ', place

                        kind = row_val[6]
                        # print 'kind = ', kind

                        money = row_val[11]
                        # print 'money = ', money

                        last_money = row_val[12]
                        # print 'last_money = ', last_money

                        sql = "insert into shen_zhen (enterprise, number, name, id, place, kind, money, last_money, update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, number, name, id, place, kind, money, last_money, update_time, filename)
                        try:
                            self.insert_into_database(sql)
                            print 'sql', sql
                            print u'*****************此条写入成功!!!*****************'

                        except Exception, e:
                            print e
                            print u'!!!!!!!!!!!!!!!此条已存在!!!!!!!!!!!'
                            self.failed_times += 1
                            print u'累计失败%s' % self.failed_times


                    elif ncols == 14:
                        cc = row_val[1]
                        c = cc[0]
                        if c.isdigit() is True:
                            try:
                                number = int(row_val[1])
                            except:
                                number = row_val[1]
                            # print 'number = ', number

                            enterprise = row_val[2]
                            # print 'enterprise = ', enterprise
                        else:
                            try:
                                number = int(row_val[2])
                            except:
                                number = row_val[2]
                            # print 'number = ', number

                            enterprise = row_val[1]
                            # print 'enterprise = ', enterprise

                        name = row_val[3].strip()
                        # print 'name = ', name

                        try:
                            id = int(row_val[5])
                        except:
                            id = row_val[5]
                        # print 'id = ', id

                        place = row_val[6].strip()
                        # print 'place = ', place

                        try:
                            kind = row_val[7].split('|')[1]
                            # print 'kind = ', kind
                        except:
                            kind = row_val[7]

                        money = row_val[12]
                        # print 'money = ', money

                        last_money = row_val[13]
                        # print 'last_money = ', last_money

                        sql = "insert into shen_zhen (enterprise, number, name, id, place, kind, money, last_money, update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, number, name, id, place, kind, money, last_money, update_time, filename)
                        try:
                            self.insert_into_database(sql)
                            print 'sql', sql
                            print u'*****************此条写入成功!!!*****************'

                        except Exception, e:
                            print e
                            print u'!!!!!!!!!!!!!!!此条已存在!!!!!!!!!!!'
                            self.failed_times += 1
                            print u'累计失败%s' % self.failed_times


                    else:
                        pass


                    if self.failed_times == 100 :
                        print u'累计失败100次,退出程序'
                        sys.exit()


            except Exception , e:
                print e
                print u'出现未知错误!!!!!!!!!!!!!!!!!!!!!!'
                print '*************************************************'





if __name__ == '__main__':
    update_searcher = ShenZhenSearcher()
    update_searcher.download_XLS()
    update_searcher.get_details()
