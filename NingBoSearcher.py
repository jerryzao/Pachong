#coding=utf-8

import requests
import os
import sys
from bs4 import BeautifulSoup
import time
from win32com import client as wc
import MySQLdb

class NingBoSearcher(object):
    def __init__(self):
        self.num = 1
        self.failed_times = 0


    def create_cursor(self):
        self.conn = MySQLdb.connect(host='172.16.0.76',port=3306,user='guanhuaixuan',passwd='123QWEasd',db='qianshui',charset='utf8')
        self.cursor=self.conn.cursor()

    def insert_into_database(self,sql):
        # print sql
        self.cursor.execute(sql)
        self.conn.commit()

    def get_docaddrs(self):
        doc_addrs_list = []
        # self.num_path = os.path.join(sys.path[0], '../Ning_Bo/num.txt')
        # num_path = self.num_path
        # with open(num_path, 'rb') as f:
        #         num = int(f.read())
        #         f.close()
        if int(self.num) == 1:
            url = 'http://www.nb-n-tax.gov.cn/xxgk/tzgg/qsgg/index.htm'
            headers = {'Host': 'www.nb-n-tax.gov.cn',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://www.nb-n-tax.gov.cn/xxgk/tzgg/qsgg/index.htm',
                    'Cookie': '_gscu_714247997=77538080gyl5fs15; _gscs_714247997=775380802237l215|pv:18; _gscbrs_714247997=1; __FTabceffgh=2016-10-27-11-14-40; __NRUabceffgh=1477538080686; __RTabceffgh=2016-10-27-11-14-40; _gscu_523705324=77538080m41zrm15; _gscs_523705324=77538080ulzoej15|pv:18; _gscbrs_523705324=1',
                    'Connection': 'keep-alive',
                    'If-Modified-Since': 'Thu, 27 Oct 2016 03:17:02 GMT',
                    'If-None-Match': '"8397-53fd02cdd4780-gzip"'}

            r = requests.session().get(url=url,headers=headers)
            # print r
            soup = BeautifulSoup(r.text,'html5lib')
            # print soup
            n = soup.find(class_='DSjc04')
            for m in n.find_all('tr'):
                m_2 = m.a.get('href')
                m_3 = m_2.split('.',1)[1]
                # print m_3
                url_2 = 'http://www.nb-n-tax.gov.cn/xxgk/tzgg/qsgg' + m_3
                print url_2
                doc_url_start = url_2.split('/t2')[0]
                # print doc_url_start
                r_2 = requests.session().get(url=url_2,headers=headers)
                soup_2 = BeautifulSoup(r_2.content, 'html5lib')
                # print soup_2
                m_4 = soup_2.find(class_='TRS_Editor')
                m_5 = m_4.a.get('href')
                # print m_5
                doc_url_end = m_5.split('.',1)[1]
                # print doc_url_end
                doc_addr = doc_url_start + doc_url_end
                # print '****', doc_addr
                doc_addrs_list.append(doc_addr)
            print u'第%s页更新完成' % 1
        else:
            pass

        while True:
            # with open(num_path, 'rb') as f:
            #     num = int(f.read())
            #     f.close()
            try:
                url_3 = 'http://www.nb-n-tax.gov.cn/xxgk/tzgg/qsgg/index_' + str(self.num) +'.htm'
                # print url_3
                headers = {'Host': 'www.nb-n-tax.gov.cn',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': 'http://www.nb-n-tax.gov.cn/xxgk/tzgg/qsgg/index.htm',
                        'Cookie': '_gscu_714247997=77538080gyl5fs15; _gscs_714247997=775380802237l215|pv:18; _gscbrs_714247997=1; __FTabceffgh=2016-10-27-11-14-40; __NRUabceffgh=1477538080686; __RTabceffgh=2016-10-27-11-14-40; _gscu_523705324=77538080m41zrm15; _gscs_523705324=77538080ulzoej15|pv:18; _gscbrs_523705324=1',
                        'Connection': 'keep-alive',
                        'If-Modified-Since': 'Thu, 27 Oct 2016 03:17:02 GMT',
                        'If-None-Match': '"8397-53fd02cdd4780-gzip"'}
                r_3 = requests.session().get(url=url_3,headers=headers)
                # print r
                soup_3 = BeautifulSoup(r_3.text,'html5lib')
                # print soup
                n_2 = soup_3.find(class_='DSjc04')
                for m_6 in n_2.find_all('tr'):
                    m_7 = m_6.a.get('href')
                    m_8 = m_7.split('.',1)[1]
                    # print m_8
                    url_4 = 'http://www.nb-n-tax.gov.cn/xxgk/tzgg/qsgg' + m_8
                    print url_4
                    doc_url_start_2 = url_4.split('/t2')[0]
                    # print doc_url_start_2
                    r_4 = requests.session().get(url=url_4,headers=headers)
                    soup_4 = BeautifulSoup(r_4.content, 'html5lib')
                    # print soup_4
                    try:
                        m_9 = soup_4.find(class_='TRS_Editor')
                        m_10 = m_9.a.get('href')
                        # print m_10
                        doc_url_end_2 = m_10.split('.',1)[1]
                        # print doc_url_end_2
                        doc_addr_2 = doc_url_start_2 + doc_url_end_2
                        # print '****', doc_addr_2
                        doc_addrs_list.append(doc_addr_2)
                    except:
                        try:
                            m_9 = soup_4.find(class_='red')
                            m_10 = m_9.a.get('href')
                            # print m_10
                            doc_url_end_2 = m_10.split('.',1)[1]
                            # print doc_url_end_2
                            doc_addr_2 = doc_url_start_2 + doc_url_end_2
                            # print '****', doc_addr_2
                            doc_addrs_list.append(doc_addr_2)
                        except:
                            pass
                print u'第%s页更新完成' % (self.num + 1)
                self.num += 1
                # with open(num_path, 'wb') as f:
                #     f.write(str(num))
                #     f.close()
            except:
                break


        print len(doc_addrs_list), '&&&', doc_addrs_list
        return doc_addrs_list

    def save_doc(self,folder,doc_addrs_list):
        headers={
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                }
        for each in doc_addrs_list:
            try:
                filename = each.split('/', 7)[7]
                with open(filename, 'wb') as f:
                    doc = requests.get(url=each, headers=headers)
                    f.write(doc.content)

                    print filename, u'文件下载成功!'
            except:
                pass

    def download_DOC(folder):
        folder = 'NingBo_DOC'
        try:
            os.mkdir(folder)
            os.chdir(folder)
        except:
            os.chdir(folder)

        doc_addrs_list = NingBoSearcher().get_docaddrs()
        NingBoSearcher().save_doc(folder, doc_addrs_list)
        print u'更新完成*********'

    def get_detail(self):
        self.create_cursor()
        doc_addrs_list = NingBoSearcher().get_docaddrs()
        print '%%%%%%%%%%%%%%%%', doc_addrs_list

        update_time = time.strftime("%Y-%m-%d")

        for each in doc_addrs_list:
            try:
                filename = each.split('/', 7)[7]
                # print 'filename = ', filename
                htmlname_start = filename.split('.', 1)[0]
                html_name = htmlname_start + '.html'
                # print 'html_name = ', html_name
            except Exception,e:
                # print e
                pass

            doc_path = sys.path[0]+ r'\NingBo_DOC'+ '\\'+ filename
            # print 'doc_path', doc_path
            html_path = sys.path[0]+ r'\NingBo_HTML'+ '\\'+ html_name
            print 'html_path = ', html_path

            word = wc.Dispatch('Word.Application')
            doc = word.Documents.Open(doc_path)
            if os.path.isfile(html_path):
                pass
            else:
                doc.SaveAs(html_path, 8)
            print u'*************转换成功!!!!!********'
            doc.Close()
            # word.Quit()
            htmlfile = open(html_path, 'r')  # 以只读的方式打开本地html文件
            htmlpage = htmlfile.read().decode('gbk', 'ignore').encode('utf8')
            # print htmlpage
            soup = BeautifulSoup(htmlpage, "html.parser")  # 实例化一个BeautifulSoup对象
            # print soup
            nn = soup.find(class_='MsoNormalTable')
            nnn = nn.find_all('tr')
            len_len = len(nnn)

            for i in xrange(1,len_len):
                element = nnn[i]
                # print element
                td_all = element.find_all('td')
                changdu = len(td_all)
                # print 'changdu = ', changdu


                if changdu == 11:
                    td = td_all[0].text.strip()
                    try:
                        td_0 = td[0]
                        # print u'序号 = ', td_0
                    except:
                        td_0 = td
                        # print u'序号 = ', td_0

                    if td_0.isdigit() is True:
                        enterprise = td_all[1].text.strip()
                        # print 'enterprise = ', enterprise

                        belongs = td_all[2].text.strip()
                        # print 'belongs = ', belongs

                        try:
                            number = int(td_all[3].text.strip())
                        except:
                            number = td_all[3].text.strip()
                        # print 'number = ', number

                        name = td_all[4].text.strip()
                        # print 'name = ', name

                        try:
                            id = int(td_all[5].text.strip())
                        except:
                            id = td_all[5].text.strip()
                        # print 'id = ', id

                        place = td_all[6].text.strip()
                        # print 'place = ', place

                        kind = td_all[7].text.strip()
                        # print 'kind = ', kind

                        money = td_all[8].text.strip()
                        # print 'money = ', money

                        Tax_time = td_all[9].text.strip()
                        # print 'Tax_time = ', Tax_time

                        last_money = td_all[10].text.strip()
                        # print 'last_money = ', last_money
                        # print '############################################'



                        sql = "insert into ning_bo (enterprise, belongs, number, name, id, place, kind, money, Tax_time, last_money,update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, belongs, number, name, id, place, kind, money, Tax_time, last_money,update_time, filename)
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


                elif changdu == 10:
                    td = td_all[0].text.strip()
                    try:
                        td_0 = td[0]
                        print u'序号 = ', td_0
                    except:
                        td_0 = td
                        print u'序号 = ', td_0

                    if td_0.isdigit() is True:
                        enterprise = td_all[1].text.strip()
                        # print 'enterprise = ', enterprise

                        belongs = td_all[2].text.strip()
                        # print 'belongs = ', belongs

                        try:
                            number = int(td_all[3].text.strip())
                        except:
                            number = td_all[3].text.strip()
                        # print 'number = ', number

                        name = td_all[4].text.strip()
                        # print 'name = ', name

                        try:
                            id = int(td_all[5].text.strip())
                        except:
                            id = td_all[5].text.strip()
                        # print 'id = ', id

                        place = td_all[6].text.strip()
                        # print 'place = ', place

                        kind = td_all[7].text.strip()
                        # print 'kind = ', kind

                        money = td_all[8].text.strip()
                        # print 'money = ', money

                        Tax_time = td_all[9].text.strip()
                        # print 'Tax_time = ', Tax_time

                        print '############################################'

                        sql = "insert into ning_bo (enterprise, belongs, number, name, id, place, kind, money, Tax_time,update_time, filename) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(enterprise, belongs, number, name, id, place, kind, money, Tax_time, update_time, filename)
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

                if self.failed_times == 2000 :
                    print u'累计失败2000次,退出程序'
                    sys.exit()
                    # pass





        word.Quit()



if __name__ == '__main__':
    NingBoSearcher().download_DOC()
    NingBoSearcher().get_detail()