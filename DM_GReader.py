#!/usr/bin/env python
# *-* coding: UTF-8 *-*
import datetime, calendar
import random
import requests
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

    def import_category(self, category_id=3, path=None, local=False):
        """Import the specific category to a Pattern Corpus for future calculation.
        category_id: the integer indicates which category to use.
        cont: the integer tells how many queries to issue to continuously crawl the GReader.
        path: the location for storing the pickle of the Pattern Corpus.
        local: to use the local stored corpus?"""

        if path is None:
            print "Please provide with a path to store/load local pickle file."
            return

        if local:
            self.corpus = Corpus.load(path)
            return

        self.target_category = self.categories[category_id]
        continuation = None

        # Crawl only the data within one day
        yesterday = calendar.timegm((datetime.date.today()-datetime.timedelta(days=1)).timetuple())

        i = 1

        while 1:

            self.target_category_content = self.reader.getCategoryContent(self.target_category, continuation=continuation)
            feeds = self.target_category_content[u'items']

            if self.target_category_content['updated'] < yesterday:
                break

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

            print i
            i = i + 1

        self.corpus.save(path, update=True)

    def _generate_clusters(self, k=10, p=1.0):
        """Use KMEANS method by default, and choose the initial k values by KMPP method.
        k is the number of clusters.
        p is to control the error of KMEANS, when p=1.0 is faster with small error.
        """
        from pattern.vector import KMEANS, KMPP
        self.clusters = self.corpus.cluster(method=KMEANS, k=10, seed=KMPP, p=1.0)

    def generate_repr_ids(self, k):
        """
        For each cluster, we choose an arbitary article as the cluster's representative.

        Return the ids of the article, here the document name is the article's id.
        Google Reader is using "i=http://www.google.com/reader/api/0/stream/items/contents" to get the content of a specific data.

        TODO How to generate representative articles, here we can only generate an arbitrary article from each cluster. Consider the centrol of the cluster?
        """
        self._generate_clusters(k=k)
        ids = [random.choice(i).name for i in self.clusters]
        return ids

    def get_article_content(self, ids):
        """docstring for get_article_content"""
        url = 'http://www.google.com/reader/api/0/stream/items/contents'
        id_handle = 'tag:google.com,2005:reader/item/%s'

        contents = []
        for _id in ids:
            r = requests.post(url, data={'i':(id_handle %_id)})
            contents.append(r.json)
        return contents
