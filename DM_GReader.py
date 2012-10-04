#!/usr/bin/env python
# *-* coding: UTF-8 *-*
from libgreader import GoogleReader, ClientAuthMethod
from pattern.vector import Document, Corpus, LEMMA
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(indent=4)

class DM_GReader():

    def __init__(self, username, password):
        auth = ClientAuthMethod(username, password)
        self.reader = GoogleReader(auth)
        self.reader.buildSubscriptionList()
        self.categories = self.reader.getCategories()
        self.corpus = Corpus()

    def import_category(self, category_id=3, cont=200, path=None, local=False):
        """Import the specific category to a Pattern Corpus for future calculation.
        category_id: the integer indicates which category to use.
        cont: the integer tells how many queries to issue to continuously crawl the GReader.
        path: the location for storing the pickle of the Pattern Corpus.
        local: to use the local stored corpus?"""

        if local:
            self.corpus = Corpus.load(path)
            pp.pprint(self.corpus.search(words=[u'iphone']))
            return

        if path is None:
            print "Please provide with a path to store/load local pickle file."
            return

        self.target_category = self.categories[category_id]
        continuation = None

        for i in range(cont):
            print i, '/', cont
            self.target_category_content = self.reader.getCategoryContent(self.target_category, continuation=continuation)
            feeds = self.target_category_content[u'items']
            print len(feeds)
            feeds_docs = []
            for feed in feeds:
                doc_name = feed[u'id'][-16:]
                for content in [u'content', u'summary']:
                    if content in feed:
                        feed_soup = BeautifulSoup(feed[content][u'content'])
                        feed_text = feed_soup.get_text()
                        feeds_docs.append(Document(feed_text, stemmer=LEMMA, name=doc_name))
                        break

            self.corpus.extend(feeds_docs)

            if u'continuation' in self.target_category_content and self.target_category_content[u'continuation'] is not None:
                continuation = self.target_category_content[u'continuation']
            else:
                print 'Finished!'
                break

        self.corpus.save(path, update=True)

