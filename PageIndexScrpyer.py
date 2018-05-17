# pylint: disable-msg=C0103
# pylint: disable-msg=C0111

from WebScrpyer import WebScrpyer


class PageIndexScrpyer(WebScrpyer):
    """[summary]
    """
    import bs4

    def getLinks(self, dom=None):
        aTags = dom.find_all('a')
        links = []
        for sTag in aTags:
            link = {
                'url': sTag.attrs.get('href'),
                'title': sTag.get_text()
            }
            links.append(link)

        return links

    def getPage(self, dom=None):
        if dom is None:
            dom = self.dom

        pageObj = super().getPage(dom)
        pageObj['links'] = self.getLinks(dom)

        return pageObj


def main():
    scryper = PageIndexScrpyer()
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))

    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    url = 'http://news.sina.com.cn/'
    page = scryper.scrypyURL(url)
    print(page)


if __name__ == "__main__":
    main()
