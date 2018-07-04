import logging 
from PageScrpyer import PageScrpyer as Scrpyer
from ElasticsearchClient import ElasticsearchClient as DBClient
from RabbitmqClient import RabbitmqClient as MqClient


class InternetScrpyer():
    mqClient = None
    scrpyer = None
    dbClient = None
    sleepSec = 0.1

    def __init__(self, config):
        self.scrpyer = Scrpyer()
        self.mqClient = MqClient(host=config.get('mq').get('host'))
        self.dbClient = DBClient(hosts=config.get('db').get('hosts'))
        return

    def scrpyPage(self, url, level=None):
        if level is None:
            level = self.mqClient.defaultLevel

        hasUrl = 0
        try:
            hasUrl = self.dbClient.hasUrl(url)
        except:
            pass

        # logging.log(logging.INFO+1,
        #             "[{:02d}][{:02d}]{:s}".format(level, hasUrl, url))

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
        res = {
            'level': None,
            'url': None,
            'error': '',
            'page': False
        }

        try: 
            task = self.mqClient.pop()
            if not task:
                time.sleep(self.sleepSec)
                return None

            level = task.get("level")
            res['level'] = level
            url = task.get("url").decode()
            res['url'] = url
            if self.scrpyPage(url, level=level):
                res["page"] = True
        except Exception as e:
            res['error'] = str(e)
        return res

    def run(self):
        while True:
            res = self.doScrpy()
            if not res:
                continue

            log = "[{:02d}][{}][{:s}]{:s}".format(
                res.get('level'), res.get('page'), res.get('error'), res.get('url'))
            if not res.get('error'):
                logging.log(logging.INFO+1, log)
            else:
                logging.warning(log)


def main():
    import json
    import sys
    config = {
        'log': {
            'level': 20
        },
        'mq': {
            'host': 'localhost'
        },
        'db': {
            'hosts': [
                'localhost:9200'
            ]
        }
    }

    if len(sys.argv) > 1:
        configPath = sys.argv[1]
        file = None

        try:
            file = open(file=configPath, mode='r')
            config = json.load(file)
        except:
            pass
        finally:
            try:
                file.close()
            except:
                pass

    # config['mq']['host'] = '9.111.111.233'
    # config['db']['hosts'] = ['9.111.213.147:9200']
    logging.basicConfig(
        level=config['log']['level'], format="%(asctime)s - %(levelname)s - %(message)s")
    logging.log(level=100, msg=config)
    scrpyer = InternetScrpyer(config=config)
    scrpyer.run()

    return 0


if __name__ == "__main__":
    main()
