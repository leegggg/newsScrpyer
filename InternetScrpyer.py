import logging


def scrpyPage(url, scrpyer, client):
    page = scrpyer.scrypyURL(url)
    client.postNews(page)
    return page


def scrpyPages(urls, scrpyer, client, level=0, maxLevel=3):
    while True:
        url = ""
        if len(urls) > 0:
            url = urls.pop(0)
        else:
            return

        hasUrl = 0
        try:
            hasUrl = client.hasUrl(url)
        except:
            pass

        logging.log(logging.INFO+1,
                    "[{:04d}][{:02d}]{:s}".format(len(urls), hasUrl, url))
        if hasUrl > 0:
            continue

        page = None
        try:
            page = scrpyPage(url, scrpyer, client)
        except Exception as e:
            logging.warning(e)
            continue
        for link in page.get("links"):
            if link.get("url"):
                urls.append(link.get("url"))

    return


def main():
    from PageScrpyer import PageScrpyer
    from ElasticsearchClient import ElasticsearchClient

    logging.basicConfig(level=logging.INFO+1)

    client = ElasticsearchClient()
    scrpyer = PageScrpyer()
    url = "https://news.sina.com.cn/"
    urls = [url]
    scrpyPages(urls, scrpyer, client, level=0, maxLevel=2)

    return 0


if __name__ == "__main__":
    main()
