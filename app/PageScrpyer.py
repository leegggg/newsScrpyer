# pylint: disable-msg=C0103
# pylint: disable-msg=C0111
import logging

from WebScrpyer import WebScrpyer


class PageScrpyer(WebScrpyer):
    """[summary]
    """
    import bs4

    dom = None

    def getLinks(self, dom=None):
        import re
        aTags = dom.find_all('a')
        links = []
        for sTag in aTags:
            url = str(sTag.attrs.get('href'))
            reHttps = re.compile(r"https{0,1}://.*")
            if reHttps.match(url):
                link = {'url': url, 'title': sTag.get_text()}
                links.append(link)

        return links

        # from dateparser.search import search_dates
        # dates = []
        # start = 0
        # end = start + lenWin
        # while end < len(html):
        #     sub = html[start:end]
        #     try:
        #         dateFind = search_dates(
        #             sub, ['zh', 'en'], settings={'STRICT_PARSING': True})
        #         if dateFind:
        #             print(dateFind)
        #     except:
        #         pass
        #     start = end
        #     end = start + lenWin
        # sub = html[start:end]
        # try:
        #     dateFind = search_dates(
        #         sub, ['zh', 'en'], settings={'STRICT_PARSING': True})
        #     if dateFind:
        #         print(dateFind)
        # except:
        #     pass

    def getContent(self, dom=None, minContentLength=512):
        if dom is None:
            dom = self.dom
        # print(self.tagWithMostP(dom).text)
        import maxNumP as pageToArticle

        content = ""
        try:
            content = pageToArticle.pageToArticle(dom).get_text(separator='\n')
        except:
            pass

        if len(content) < minContentLength:
            try:
                content = dom.get_text(separator='\n')
            except:
                pass

        return content
        # dom = bs4.BeautifulSoup(page, "html.parser")

    def getPage(self, dom=None):
        if dom is None:
            dom = self.dom

        pageObj = super().getPage(dom)
        pageObj['content'] = self.getContent(dom)
        pageObj['links'] = self.getLinks(dom)

        return pageObj


def main():
    scryper = PageScrpyer()
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))
    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    # url = 'https://www.centos.bz/2017/10/kubernetes%E4%B9%8B%E6%9A%82%E5%81%9C%E5%AE%B9%E5%99%A8/'
    # url = "http://mil.news.sina.com.cn/jssd/2018-07-06/doc-ihexfcvk7380607.shtml"
    url = "http://sports.sina.com.cn/others/volleyball/2018-07-06/doc-ihexfcvk4526321.shtml"
    # url = "http://jiaoxue.cri.cn/gngedu/child"
    # url = "https://www.cnblogs.com/junrong624/p/5533655.html"
    # url = "https://blog.csdn.net/m0_37752182/article/details/80037981"
    # url = "http://news.sina.com.cn/c/2018-07-05/doc-ihexfcvk1560155.shtml"
    # url = "https://www.sohu.com/a/208352353_697896"
    # url = "https://pypi.org/project/webstruct/"
    page = scryper.scrypyURL(url)
    import json
    print(json.dumps(page, ensure_ascii=False, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
