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
                link = {
                    'url': url,
                    'title': sTag.get_text()
                }
                links.append(link)

        return links

    def getContent(self, dom=None):
        if dom is None:
            dom = self.dom
        # print(self.tagWithMostP(dom).text)
        import maxNumP as pageToArticle

        content = ""
        try:
            content = pageToArticle.pageToArticle(dom).get_text(separator='\n')
        except:
            try:
                content = dom.get_text(separator='\n')
            except:
                pass
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
    url = 'https://www.centos.bz/2017/10/kubernetes%E4%B9%8B%E6%9A%82%E5%81%9C%E5%AE%B9%E5%99%A8/'
    url = "http://jiaoxue.cri.cn/gngedu/child"
    page = scryper.scrypyURL(url)
    import json
    print(json.dumps(page, ensure_ascii=False,
                     indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
