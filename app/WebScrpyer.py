# pylint: disable-msg=C0103
# pylint: disable-msg=C0111


class WebScrpyer:
    """[summary]
    """
    import bs4

    dom = None

    def getDom(self, url):
        import req
        self.dom = req.getDom(url)
        return self.dom

    def getMeta(self, dom=None):
        if dom is None:
            dom = self.dom

        metas = dom.findAll(name="meta", recursive=True)
        metaObj = {}
        for meta in metas:
            if meta.attrs.get('name') and meta.attrs.get('content'):
                metaObj[meta.attrs.get('name')] = meta.attrs.get('content')
        return metaObj

    def getTitle(self, dom=None):
        if dom is None:
            dom = self.dom

        title = ""
        try:
            title = dom.find(name='title').text
        except:
            pass

        return title

    def getPage(self, dom=None):
        if dom is None:
            dom = self.dom

        pageObj = {}
        pageObj['meta'] = self.getMeta(dom)
        pageObj['title'] = self.getTitle(dom)

        return pageObj

    def scrypyURL(self, url):
        from datetime import datetime
        dom = self.getDom(url)
        pageObj = self.getPage(dom)
        pageObj['url'] = url
        pageObj['timestampScrpy'] = datetime.now().timestamp()
        return pageObj


def main():
    scryper = WebScrpyer()
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))
    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    # url = 'https://www.centos.bz/2017/10/kubernetes%E4%B9%8B%E6%9A%82%E5%81%9C%E5%AE%B9%E5%99%A8/'
    url = "http://www.legaldaily.com.cn"
    page = scryper.scrypyURL(url)
    import json
    print(json.dumps(page, ensure_ascii=False,
                     indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
