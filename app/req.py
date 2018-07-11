import logging
headers = {
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language':
    'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'DNT': '1',
    # 'Pragma': 'no-cache',
    # 'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
}


def getDom(url):
    import bs4
    import requests
    import chardet
    req = requests.get(url, headers=headers, timeout=(10, 10), stream=True)
    # req = requests.get(url)
    # page = str(req.content, req.encoding)
    # print(req.encoding)

    page = None
    acceptableContentTypes = [
        'text/html', 'application/xhtml+xml', 'application/xml'
    ]

    for contentType in acceptableContentTypes:
        if req.headers['content-type'].find(contentType) >= 0:
            break
    else:
        logging.debug("ContentType:[{}]{}".format(req.headers['content-type'],
                                                  url))
        raise Exception("ContentType: {}".format(
            req.headers.get('content-type')))

    if (not req.status_code) or (not req.status_code < 400):
        raise Exception("status_code: {}".format(req.status_code))

    try:
        logging.debug("tryUtf8:{}".format(url))
        page = req.content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            logging.debug("tryGB:{}".format(url))
            page = req.content.decode('GB2312')
        except UnicodeDecodeError:
            encode = chardet.detect(req.content).get('encoding')
            logging.debug("Detected[{}]:{}".format(encode, url))
            page = req.content.decode(encode, 'ignore')

    page = page.replace('\n', '').replace('\t', '').replace('\r', '').replace(
        '\xa0', '')
    logging.debug("length of page: {}".format(len(page)))
    dom = bs4.BeautifulSoup(page, "html.parser")
    return dom


def main():
    logging.basicConfig(level=logging.DEBUG)
    # getDom('http://slide.sports.sina.com.cn/o/slide_2_53064_60676.html')
    # getDom('http://news.sina.com.cn/')
    # getDom('http://zhuanlan.sina.com.cn/')
    # getDom('http://i1.sinaimg.cn/edu/sinaopen/SinaOpencourse_V2.02.apk')
    # dom = getDom('http://news.163.com')
    dom = getDom('http://news.163.com/abb')  #404
    # getDom('http://shouji.www.yxdown.com/down?id=509322') # incorrect type
    print(dom)

    return 0


if __name__ == "__main__":
    main()
