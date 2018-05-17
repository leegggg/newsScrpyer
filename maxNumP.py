def tagWithMostP(dom, tagMaxP=None):
    for child in dom.findChildren(recursive=False):
        if child and not child.get('name') == 'p':
            numMaxP = 0
            if tagMaxP:
                numMaxP = len(tagMaxP.find_all('p', recursive=False))
            numCurrentP = len(child.find_all('p', recursive=False))
            if numCurrentP > numMaxP:
                tagMaxP = child
            tagMaxP = tagWithMostP(dom=child, tagMaxP=tagMaxP)
    return tagMaxP


def pageToArticle(dom):
    return tagWithMostP(dom)
