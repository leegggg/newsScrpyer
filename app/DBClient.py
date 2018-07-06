# pylint: disable-msg=F0002
class DBClinet():

    # es = {}
    # index = "news"
    # docType = "page"

    def __init__(self, config):
        from ElasticsearchClient import ElasticsearchClient
        from MongoDBClient import MongoDBClient
        self.es = ElasticsearchClient(
            hosts=config.get("elasticsearch").get('hosts'))
        self.mongoDB = MongoDBClient(url=config.get("mongodb").get('url'))
        self.index = config["index"]
        self.docType = config["docType"]
        return

    def postNews(self, news, index=None, docType=None):
        import copy
        if not index:
            index = self.index
        if not docType:
            docType = self.docType
        # postNews(self, news, index=None, docType=None):
        mongoDoc = copy.deepcopy(news)
        del mongoDoc['content']
        docId = self.mongoDB.postNews(mongoDoc, index=index, docType=docType)

        esDoc = copy.deepcopy(news)
        del esDoc['links']
        del esDoc['meta']
        self.es.postNews(esDoc, index=index, docType=docType, id=docId)

        return

    def getNews(self, attrs):

        return

    def hasUrl(self, url):
        return self.es.hasUrl(url)


"""
curl -XGET "localhost:9200/news/_search?pretty=true" -H 'Content-Type: application/json' -d '
{
  "query": { "match_all": {} }
}'
"""


def main():
    from PageScrpyer import PageScrpyer

    config = {
        "index": "news",
        "docType": "webNews",
        "elasticsearch": {
            "hosts": ["elk.news.linyz.net:9200"]
        },
        "mongodb": {
            "url": "mongodb://root:passw0rd@mangodb.news.linyz.net:27017/"
        }
    }

    scryper = PageScrpyer()
    client = DBClinet(config)
    # index = elasticsearch.client.IndicesClient(client.es)
    # settingFp = open("es-mapping-news.json")
    # indexSetting = json.load(settingFp)
    # settingFp.close()
    # index.create(index="news", body=indexSetting)
    # return
    # print(scryper.getIndexList(
    #    'https://ad.toutiao.com/overture/index/account_balance/'))
    # print(scryper.login(user='g07xw6@163.com', passwd='Bonnie123.'))
    # curl -XPUT http://localhost:9200/news -H 'Content-Type:application/json' -d "@./es-mapping-news.json"
    # curl -XPOST http://localhost:9200/news -H 'Content-Type:application/json' -d'
    url = 'https://www.centos.bz/2017/10/kubernetes%E4%B9%8B%E6%9A%82%E5%81%9C%E5%AE%B9%E5%99%A8/'
    page = scryper.scrypyURL(url)
    import json
    print(json.dumps(page, ensure_ascii=False, indent=4, sort_keys=True))
    client.postNews(page)
    print(client.hasUrl(url))

    return


if __name__ == "__main__":
    main()
