# pylint: disable-msg=C0103
# pylint: disable-msg=C0111

from WebScrpyer import WebScrpyer


class NewsScrpyer(WebScrpyer):
    """[summary]
    """
    import bs4

    dom = None

    def getContent(self, dom=None):
        if dom is None:
            dom = self.dom
        # print(self.tagWithMostP(dom).text)
        import maxNumP as pageToArticle

        return pageToArticle.pageToArticle(dom).get_text(separator='\n')
        # dom = bs4.BeautifulSoup(page, "html.parser")

    def getPage(self, dom=None):
        if dom is None:
            dom = self.dom

        pageObj = super().getPage(dom)
        pageObj['content'] = self.getContent(dom)

        return pageObj


def main():
    scryper = NewsScrpyer()
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))
    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    url = 'https://www.centos.bz/2017/10/kubernetes%E4%B9%8B%E6%9A%82%E5%81%9C%E5%AE%B9%E5%99%A8/'
    page = scryper.scrypyURL(url)
    import json
    print(json.dumps(page, ensure_ascii=False, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
