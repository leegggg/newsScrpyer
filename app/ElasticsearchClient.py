# pylint: disable-msg=F0002
class ElasticsearchClient():

    # es = {}
    # index = "news"
    # docType = "page"

    def __init__(self,
                 hosts=["localhost:9200"],
                 index="news",
                 docType="webNews"):
        from elasticsearch import Elasticsearch
        self.es = Elasticsearch(hosts=hosts)
        self.index = index
        self.docType = docType
        return

    def postNews(self, news, index=None, docType=None, id=None):
        import uuid
        if not index:
            index = self.index
        if not docType:
            docType = self.docType
        if not id:
            id = str(uuid.uuid4())

        self.es.index(index=index, doc_type=docType, id=id, body=news)

        return

    def getNews(self, attrs):

        return

    def hasUrl(self, url):
        searchBody = {"size": 0, "query": {"term": {"url": url}}}
        indexPatten = self.index + "*"
        res = self.es.search(index=indexPatten, body=searchBody)

        hits = 0
        try:
            hits = res['hits']['total']
        except:
            pass

        return hits


"""
curl -XGET "localhost:9200/news/_search?pretty=true" -H 'Content-Type: application/json' -d '
{
  "query": { "match_all": {} }
}'
"""


def main():
    from PageScrpyer import PageScrpyer
    scryper = PageScrpyer()
    client = ElasticsearchClient()
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
