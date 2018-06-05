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

    def scrpyPage(self, url):
        hasUrl = 0
        try:
            hasUrl = self.dbClient.hasUrl(url)
        except:
            pass

        page = self.scrpyer.scrypyURL(url)
        self.dbClient.postNews(page)

        for link in page.get("links"):
            if not link.get("url"):
                continue
            subUrl = link.get("url")
            hasUrl = self.dbClient.hasUrl(subUrl)
            if hasUrl < 1:
                self.mqClient.push(subUrl)

        return page

    def doScrpy(self):
        import time
        url = self.mqClient.pop()
        if not url:
            time.sleep(self.sleepSec)
            return None
        url = url.decode()

        hasUrl = 0
        try:
            hasUrl = self.dbClient.hasUrl(url)
        except:
            pass

        logging.log(logging.INFO+1, "[{:02d}]{:s}".format(hasUrl, url))

        if hasUrl > 0:
            return None

        return self.scrpyPage(url)

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
