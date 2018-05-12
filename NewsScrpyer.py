# pylint: disable-msg=C0103
# pylint: disable-msg=C0111


class NewsScrpyer:
    """[summary]
    """
    import bs4

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
    }
    dom = None

    def getDom(self, url):
        import bs4
        import requests

        page = requests.get(url, headers=self.headers).content.replace('\n', '').replace(
            '\t', '').replace('\r', '').replace('\xa0', '')
        self.dom = bs4.BeautifulSoup(page, "html.parser")
        return self.dom

    def tagWithMostP(self, dom, tagMaxP=None):
        for child in dom.findChildren(recursive=False):
            if child and not child.get('name') == 'p':
                numMaxP = 0

                if tagMaxP:
                    numMaxP = len(tagMaxP.find_all('p', recursive=False))

                numCurrentP = len(child.find_all('p', recursive=False))
                if numCurrentP > numMaxP:
                    tagMaxP = child

                tagMaxP = self.tagWithMostP(dom=child, tagMaxP=tagMaxP)
        return tagMaxP

    def getContent(self, dom=None):
        if dom is None:
            dom = self.dom

        return self.tagWithMostP(dom).text
        # dom = bs4.BeautifulSoup(page, "html.parser")


def Main():
    scryper = NewsScrpyer()
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))
    import requests
    import bs4
    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    url = 'http://blog.sina.com.cn/s/blog_7d75a1df0102y1y7.html?tj=1'
    dom = scryper.getDom(url)
    print(scryper.getContent(dom))


Main()
