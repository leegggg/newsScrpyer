import logging
from PageScrpyer import PageScrpyer as Scrpyer
from ElasticsearchClient import ElasticsearchClient as DBClient
from RabbitmqClient import RabbitmqClient as MqClient


class InternetScrpyer():
    mqClient = None
    scrpyer = None
    dbClient = None
    sleepSec = 0.1

    def __init__(self):
        self.scrpyer = Scrpyer()
        self.mqClient = MqClient(host="172.17.0.1")
        self.dbClient = DBClient()
        return

    def scrpyPage(self, url, level=None):
        if level is None:
            level = self.mqClient.defaultLevel

        hasUrl = 0
        try:
            hasUrl = self.dbClient.hasUrl(url)
        except:
            pass

        logging.log(logging.INFO+1,
                    "[{:02d}][{:02d}]{:s}".format(level, hasUrl, url))

        if level > 0 and hasUrl > 0:
            return {}

        page = self.scrpyer.scrypyURL(url)
        self.dbClient.postNews(page)
        subLevel = level + 1
        for link in page.get("links"):
            if not link.get("url"):
                continue
            subUrl = link.get("url")
            hasUrl = self.dbClient.hasUrl(subUrl)
            if hasUrl < 1:
                self.mqClient.push(data=subUrl, level=subLevel)

        return page

    def doScrpy(self):
        import time
        task = self.mqClient.pop()
        if not task:
            time.sleep(self.sleepSec)
            return None

        level = task.get("level")
        url = task.get("url").decode()

        return self.scrpyPage(url, level=level)

    def run(self):
        while True:
            try:
                self.doScrpy()
            except:
                pass


def main():

    logging.basicConfig(level=logging.INFO+1)

    scrpyer = InternetScrpyer()
    scrpyer.run()

    return 0


if __name__ == "__main__":
    main()
