
import urllib.request
import os
import re
import sys
import time


def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400')
    response = urllib.request.urlopen(url)
    html = response.read()

    return html


def find_pics(url):
    html = url_open(url).decode('gbk')
    pic_addrs = []
    back = 0
    reg = r'http://ymz.qqwmb.com/allimg/c[0-9][0-9][0-9][0-9][0-9][0-9].*.jpg'
    for each in re.findall(reg,html):
        url = each
        urllib.parse.quote(url)
        pic_addrs.append(url)

        
    return pic_addrs



def save_pics(folder, pic_addrs):
    for each in pic_addrs:
        filename = each.split('/')[5]
        with open(filename, 'wb') as f:
            pic = url_open(each)
            f.write(pic)

            
def download_PIC(folder='123'):
    try:
        os.mkdir(folder)
        os.chdir(folder)
        
    except:os.chdir(folder)
    
    url = 'http://www.youmzi.com/meinv.html'
    reg = 'meinv_[0-9][0-9][0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?.html'

    pages = range(0,50,1)
    for page in pages:
        url = "http://www.youmzi.com/meinv_"+str(page+1)+'.html'
        pic_addrs = find_pics(url)
        save_pics(folder, pic_addrs)
        time.sleep(1)

if __name__ == '__main__':
    download_PIC()
