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

        return dom.find(name='title').text

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
