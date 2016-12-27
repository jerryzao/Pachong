#coding=utf-8


import requests
from bs4 import BeautifulSoup
import re
import MySQLdb
import sys
import time

class shzj(object):
    def __init__(self):
        self.failed_times = 0


    def create_cursor(self):
        self.conn = MySQLdb.connect(host='172.16.0.76',port=3306,user='guanhuaixuan',passwd='123QWEasd',db='guojia_zj',charset='utf8')
        self.cursor=self.conn.cursor()

    def insert_into_database(self,sql):
        # print sql
        self.cursor.execute(sql)
        self.conn.commit()

    def findLinks(self,htmlString):
        """
        搜索htmlString中所有的链接地址
        """
        linkPattern = re.compile("href='.+?'")
        return linkPattern.findall(htmlString)

    def get_detail_addrs(self,num):
        self.create_cursor()
        detail_addrs_list = []
        url = 'http://www.shzj.gov.cn/col/col358/index.html'
        url_2 = 'http://www.shzj.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp'
        headers = {'Host': 'www.shzj.gov.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate',
                'Cookie': '_gscu_874338513=7764321532k7g122; Hm_lvt_44a6994269273ce154ca08b03d85ff8f=1477643982,1477877319; _gscbrs_874338513=1; Hm_lpvt_44a6994269273ce154ca08b03d85ff8f=1477877329',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=0'}

        payload = {
                    "startrecord":str(num),
                    # "endrecord":"180",
                    "perpage":"20",
                    "col":"1",
                    "appid":"1",
                    "webid":"1",
                    "path":"/",
                    "columnid":"358",
                    "sourceContentType":"1",
                    "unitid":"5835",
                    "webname":"上海市质量技术监督局",
                    "permissiontype":"0"
                   }
        r_2 = requests.session().post(url=url_2, headers=headers, data=payload)
        # print r_2
        # r = requests.session().get(url=url, headers=headers)
        # print r.text
        soup = BeautifulSoup(r_2.content, 'xml')
        # print '%%%%', soup
        # m = soup.find(class_='padding10')
        # print m.text
        m_2 = shzj().findLinks(soup.text)
        # print '#####', m_2
        for i in range(len(m_2)):
            detail_addrs_2 = m_2[i]
            detail_addrs = detail_addrs_2.split("'",3)[1]
            detail = detail_addrs
            print 'detail=',detail_addrs

            detail_addrs_list.append(detail_addrs)
            rr = requests.session().get(url=detail_addrs, headers=headers)
            qqq = BeautifulSoup(rr.content, 'html5lib')
            try:
                body = qqq.find(id='ivs_content')
                # print body
                div = body.find_all('div')
                # print 'len(div)= ', len(div)
                table = body.find_all('table')
                # print 'len(table)= ', len(table)
                if len(div) == 0 :
                    biaoge = table
                else:
                    biaoge = div

                for element_div in biaoge:
                    tr = element_div.find_all('tr')
                    # print 'len(tr)', len(tr)

                    try:
                        td_len = tr[0].find_all('td')
                        # print 'len(td_len)= ', len(td_len)
                        judgment = td_len[len(td_len)- 1].text.strip()
                        judgment_2 = td_len[len(td_len)- 2].text.strip()
                        # print 'judgment= ', judgment

                    except:
                        pass

                    if judgment == u'不合格项目':
                        kind = u'抽查不合格产品'
                        for y in range(1,len(tr)):
                            element_tr = tr[y]
                            # print element_tr
                            iii = element_tr.find_all('td')
                            # print u'详情表字段数=', len(iii)

                            if len(iii) == 7:
                                product = iii[0].text.strip()
                                # print 'product= ', product
                                trademark = iii[1].text.strip()
                                # print 'trademark= ', trademark
                                ggxh = iii[2].text.strip()
                                # print 'ggxh= ', ggxh
                                product_time = iii[3].text.strip()
                                # print 'product_time= ', product_time
                                product_enterprise = iii[4].text.strip()
                                # print 'product_enterprise= ', product_enterprise
                                check_enterprise = iii[5].text.strip()
                                # print 'check_enterprise= ', check_enterprise
                                unqualified_product = iii[6].text.strip()
                                # print 'unqualified_product= ', unqualified_product

                            elif len(iii) == 8:
                                product = iii[1].text.strip()
                                # print 'product= ', product
                                trademark = iii[2].text.strip()
                                # print 'trademark= ', trademark
                                ggxh = iii[3].text.strip()
                                # print 'ggxh= ', ggxh
                                product_time = iii[4].text.strip()
                                # print 'product_time= ', product_time
                                product_enterprise = iii[5].text.strip()
                                # print 'product_enterprise= ', product_enterprise
                                check_enterprise = iii[6].text.strip()
                                # print 'check_enterprise= ', check_enterprise
                                unqualified_product = iii[7].text.strip()
                                # print 'unqualified_product= ', unqualified_product
                            else:
                                pass

                            # title_2 = qqq.find(id='ivs_title')
                            # title = title_2.text
                            # print 'title=', title
                            update_time = time.strftime("%Y-%m-%d")
                            # print a
                            sql_chaxun = "SELECT kind, product, trademark, ggxh, product_time, product_enterprise,check_enterprise, unqualified_product from sh_zj"
                            nums = self.cursor.execute(sql_chaxun)
                            # print 'nums= ', nums
                            info = self.cursor.fetchmany(nums)
                            # print info
                            pandin_num = 0
                            for i in range(0,nums):
                                if info[i][0] == kind and info[i][1] == product and info[i][2] == trademark and info[i][3] == ggxh and info[i][4] == product_time and info[i][5] == product_enterprise and info[i][6] == check_enterprise:
                                    pandin_num = pandin_num + 1
                                else:
                                    pass

                            if pandin_num == 0:
                                sql = "insert into sh_zj (kind, product, trademark, ggxh, product_time, product_enterprise,check_enterprise, unqualified_product, update_time) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(kind, product, trademark, ggxh, product_time, product_enterprise,check_enterprise, unqualified_product, update_time)
                                try:
                                    self.insert_into_database(sql)
                                    print 'sql', sql
                                    print u'*****************此条写入成功!!!*****************'

                                except Exception, e:
                                    print e
                                    print u'!!!!!!!!!!!!!!!写入数据库异常!!!!!!!!!!!'
                            else:
                                print u'!!!!!!!!!此条数据已存在!!!!!!!!!'
                                self.failed_times += 1
                                print u'累计失败%s' % self.failed_times


                    elif judgment == u'备注' and judgment_2 == u'不合格项目':
                        kind = u'抽查不合格产品'
                        for y in range(1,len(tr)):
                            element_tr = tr[y]
                            # print element_tr
                            iii = element_tr.find_all('td')
                            # print u'详情表字段数=', len(iii)

                            if len(iii) == 8:
                                product = iii[0].text.strip()
                                # print 'product= ', product
                                trademark = iii[1].text.strip()
                                # print 'trademark= ', trademark
                                ggxh = iii[2].text.strip()
                                # print 'ggxh= ', ggxh
                                product_time = iii[3].text.strip()
                                # print 'product_time= ', product_time
                                product_enterprise = iii[4].text.strip()
                                # print 'product_enterprise= ', product_enterprise
                                check_enterprise = iii[5].text.strip()
                                # print 'check_enterprise= ', check_enterprise
                                unqualified_product = iii[6].text.strip()
                                # print 'unqualified_product= ', unqualified_product

                            else:
                                pass

                            update_time = time.strftime("%Y-%m-%d")
                            # print a
                            sql_chaxun = "SELECT kind, product, trademark, ggxh, product_time, product_enterprise,check_enterprise, unqualified_product from sh_zj"
                            nums = self.cursor.execute(sql_chaxun)
                            # print 'nums= ', nums
                            info = self.cursor.fetchmany(nums)
                            # print info
                            pandin_num = 0
                            for i in range(0,nums):
                                if info[i][0] == kind and info[i][1] == product and info[i][2] == trademark and info[i][3] == ggxh and info[i][4] == product_time and info[i][5] == product_enterprise and info[i][6] == check_enterprise:
                                    pandin_num = pandin_num + 1
                                else:
                                    pass

                            if pandin_num == 0:
                                sql = "insert into sh_zj (kind, product, trademark, ggxh, product_time, product_enterprise,check_enterprise, unqualified_product, update_time) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(kind, product, trademark, ggxh, product_time, product_enterprise,check_enterprise, unqualified_product, update_time)
                                try:
                                    self.insert_into_database(sql)
                                    print 'sql', sql
                                    print u'*****************此条写入成功!!!*****************'

                                except Exception, e:
                                    print e
                                    print u'!!!!!!!!!!!!!!!写入数据库异常!!!!!!!!!!!'
                            else:
                                print u'!!!!!!!!!此条数据已存在!!!!!!!!!'
                                self.failed_times += 1
                                print u'累计失败%s' % self.failed_times


                    else:
                        pass

                    if self.failed_times == 20 :
                        print u'累计失败20次,退出程序'
                        sys.exit()

            except Exception, e:
                print '########################################'
                print e
                print u'!!!!!!!!!!!!!!!写入数据库异常!!!!!!!!!!!'


        print u'第%s条更新完成' % num

    def download(self):
        for num in range(1,601,60):
            shzj().get_detail_addrs(num)


if __name__ == '__main__':
    shzj().download()