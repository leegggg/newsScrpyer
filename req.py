
headers = {
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    # 'DNT': '1',
    # 'Pragma': 'no-cache',
    # 'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
}


def getDom(url):
    import bs4
    import requests
    req = requests.get(url, headers=headers)
    # req = requests.get(url)
    # page = str(req.content, req.encoding)
    # print(req.encoding)
    page = str(req.content, 'utf-8')
    page = page.replace('\n', '').replace(
        '\t', '').replace('\r', '').replace('\xa0', '')
    dom = bs4.BeautifulSoup(page, "html.parser")
    return dom
