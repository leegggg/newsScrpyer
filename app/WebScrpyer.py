# pylint: disable-msg=C0103
# pylint: disable-msg=C0111
import logging


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
        import re
        if dom is None:
            dom = self.dom

        metas = dom.findAll(name="meta", recursive=True)
        metaObj = {}
        regex = re.compile(r"[^a-zA-Z0-9]")
        for meta in metas:
            if meta.attrs.get('name') and meta.attrs.get('content'):
                key = meta.attrs.get('name')
                key = regex.sub("_", key)
                value = meta.attrs.get('content')
                metaObj[key] = value
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

    def getTimestamp(self, dom=None, lenWin=2048, tsFallback=None):
        import re
        import dateparser
        import datetime

        if dom is None:
            dom = self.dom

        html = str(dom)
        dateRegexps = [
            r"[0-9]{4}年[0-9]{2}月[0-9]{2}日.{0,8}[0-9]{2}:[0-9]{2}",
            r"[0-9]{4}年[0-9]{2}月[0-9]{2}日",
            r"[0-9]{4}年[0-9]{2}月[0-9]{2}日.{0,8}[0-9]{2}:[0-9]{2}:[0-9]{2}",
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}.{0,8}0-9]{2}:[0-9]{2}",
            r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
            # r"(([0]?[0-5][0-9]|[0-9]):([0-5][0-9]))"
        ]

        dates = {}

        for regexp in dateRegexps:
            reDate = re.compile(regexp)
            match = reDate.findall(html)
            if match:
                for dateStr in match:
                    try:
                        ts = dateparser.parse(dateStr).timestamp()
                    except:
                        continue

                    if dates.get(ts):
                        dates[ts] += 1
                    else:
                        dates[ts] = 1
            else:
                continue

        if not dates:
            logging.warn("Try to find Unix Timestamp result may be incorrect")
            # Timestamp in sec
            reDate = re.compile(r"[0-9]{9,10}")
            match = reDate.findall(html)
            if match:
                for dateStr in match:
                    ts = int(dateStr)
                    now = datetime.datetime.now().timestamp()
                    if ts > now + 3600 * 24 * 360 or ts < now - 3600 * 24 * 3600 * 30:
                        continue
                    if dates.get(ts):
                        dates[ts] += 1
                    else:
                        dates[ts] = 1

            # Timestamp in millis
            reDate = re.compile(r"[0-9]{12,13}")
            match = reDate.findall(html)
            if match:
                for dateStr in match:
                    ts = int(dateStr) / 1000
                    now = datetime.datetime.now().timestamp()
                    if ts > now + 3600 * 24 * 360 or ts < now - 3600 * 24 * 3600 * 30:
                        continue
                    if dates.get(ts):
                        dates[ts] += 1
                    else:
                        dates[ts] = 1

        maxCount = 0
        ts = float("-inf")
        for key, value in dates.items():
            if value > maxCount:
                maxCount = value
                ts = key
        if maxCount == 0:
            logging.warn("Timestamp not found fall back will be used.")
            ts = tsFallback

        return ts

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
        pageObj['bodyTs'] = self.getTimestamp(dom)
        if not pageObj['bodyTs']:
            pageObj['bodyTsFallback'] = True
            pageObj['bodyTs'] = datetime.now().timestamp()
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
    print(json.dumps(page, ensure_ascii=False, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
