class MongoDBClient():
    def __init__(self, url="mongodb://localhost:27017/"):
        import pymongo
        self.client = pymongo.MongoClient(url)
        return

    def postNews(self, doc, index="news", docType="webNews"):
        # import datetime
        # try:
        #     doc["bodyTs"] = datetime.datetime.fromtimestamp(doc["bodyTs"])
        # except:
        #     pass
        #
        # try:
        #     doc["timestampScrpy"] = datetime.datetime.fromtimestamp(
        #         doc["bodyTs"])
        # except:
        #     pass

        db = self.client.get_database(index)
        collection = db.get_collection(docType)
        docID = collection.insert_one(doc).inserted_id

        return docID


def main():
    from PageScrpyer import PageScrpyer
    scryper = PageScrpyer()
    client = MongoDBClient(
        "mongodb://root:passw0rd@mangodb.news.linyz.net:27017/")
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
    id = client.postNews(page)
    print("Doc ID is {}".format(id))
    # print(client.hasUrl(url))

    return


if __name__ == "__main__":
    main()
