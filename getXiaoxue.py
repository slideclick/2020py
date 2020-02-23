import requests
from lxml import etree
import time
import threading
import os.path

totalThread = 5
threadLock = threading.Lock()

def getLinks(url,num):
    html = requests.get(url)
    html.encoding = 'UTF-8'
    dom = etree.HTML(html.text)
    dom
    print(dom)
    pdfs = dom.xpath('//*[@id="container"]/div[%d]/ul/li/div/a[2]/@href' %num)
    pdfs = [s[2:] for s in pdfs]
    print(pdfs)
    #str = '//*[@id="container"]/div[%d]/ul/li/h6/a/text()', %num
    names = dom.xpath('//*[@id="container"]/div[%d]/ul/li/h6/a/text()' %num)
    pdfs = [url + s for s in pdfs]
    print(names, pdfs)
   # names = ['yuwen','shuxue']
    #pdfs=['https://bp.pep.com.cn/jc/ptgzkcbzsyjks/gzkbywjc/202002/P020200211701779192796.pdf','https://bp.pep.com.cn/jc/ptgzkcbzsyjks/gzkbywjc/202002/P020200211701963887347.pdf']
    return names, pdfs

def getUniqPdfName(name):
    pdfName = name + '.pdf'
    i = 1
    while(os.path.exists(pdfName)):
        pdfName = f'{name} ({i}).pdf'
        i += 1
    return pdfName

def downloadPdf(name, url, threadName):
    name = getUniqPdfName(name)
    t = time.time()
    pdf = requests.get(url).content
    fp = open(name, 'wb')
    fp.write(pdf)
    t = time.time() - t
    print(f'{threadName} Downloaded {url} ==> {name} in {t:.3f} s.')

def downloadPdfs(names, links, threadName):
    print(f'{threadName} Start downloading pdf files...')
    while(len(links) > 0):
        threadLock.acquire()
        name = names.pop(0)
        url = links.pop(0)
        threadLock.release()
        downloadPdf(name, url, threadName)
        print(f'Left {len(links)} files.')

def getPdfs(names, links):
    n = len(links)
    print(f'Total {n} pdf files to be downloaded.')
    t = time.time()
    threadList = []
    for i in range(totalThread):
        th = threading.Thread(target=downloadPdfs, args=(names, links, f'[Thread {i}]', ))
        th.setDaemon(True)
        threadList.append(th)
        th.start()
    for th in threadList:
        th.join()
    t = time.time() - t
    print(f'Successfully downloaded {n} pdf files in {t:.3f} s.')

def main():
    url = 'https://bp.pep.com.cn/jc/ywjygjkcjc/'
    for num in range(2,17):
        names, links = getLinks(url,num)
        getPdfs(names, links)

if __name__ == '__main__':
    main()
