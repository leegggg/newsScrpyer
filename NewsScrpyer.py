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

    def tagWithMostP(self, dom):
        import bs4
        for child in dom.children:
            print(child.get('name'))
        #dom = bs4.BeautifulSoup(page, "html.parser")


def Main():
    scryper = NewsScrpyer()
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))
    import requests
    import bs4
    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    url = 'http://www.xinhuanet.com/house/2018-04-23/c_1122723902.htm'
    page = requests.get(url, headers=scryper.headers).content
    dom = bs4.BeautifulSoup(page, "html.parser")
    scryper.tagWithMostP(dom)


Main()
