#!/usr/bin/env python
# *-* coding: UTF-8 *-*
import datetime
import calendar
import random
import numpy as np
import pprint
import sys
from Tree import Tree

try:
    import requests
    from libgreader import GoogleReader, ClientAuthMethod
    from pattern.vector import centroid, distance, Document, Corpus, LEMMA
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("""You need install these dependencies first!
                Pakeges:
                1. requests   # Issue http requesets
                2. libgreader # Connecting Google reader services
                3. pattern    # Storing documents into corpus format
                4. beautifulsoup4 # Paring Html into plain text
                install them with pip or easy_install.
                sudo easy_install requests libgreader pattern beautifulsoup4""")

pp = pprint.PrettyPrinter(indent=4)


class myTree(Tree):
    def __init__(self, data):
        super(myTree, self).__init__(data)
        self.copied = False


class Covertree():
    """Data structure, recommend using distance within (0,1) """
    def __init__(self, distance, maxlevel):
        self.ct = None
        self.levels = [set() for i in range(maxlevel)]
        self.distance = distance
        self.maxlevel = maxlevel

    def insert(self, tree_node, tree, i):
        if self.ct == None:
            self.ct = tree_node
            new_tmp_p = myTree(self.ct.data)
            self.ct.addChild(new_tmp_p)
            self.ct.copied = True
            self.levels[0].add(tree_node)
            self.levels[1].add(new_tmp_p)
            return
        elif i == self.maxlevel - 2:
            tree.addChild(tree_node)
            self.levels[-1].add(tree_node)
            return
        else:
            for p in tree.getChildren():
                d = self.distance(p.data, tree_node.data)
                if d < 2 ** (-i - 1):
                    # Add p to p's children
                    if not p.copied:
                        new_p = myTree(p.data)
                        p.addChild(new_p)
                        p.copied = True
                        self.levels[i + 2].add(new_p)
                    # Recursively
                    self.insert(tree_node, p, i + 1)
                    return
            tree.addChild(tree_node)
            self.levels[i + 1].add(tree_node)

    def merge_levels(self):
        for i, level in enumerate(self.levels):
            if i > 0:
                if self.levels[i] == set():
                    return
                data_i = [_.data for _ in self.levels[i]]
                for item in self.levels[i - 1]:
                    if item.data not in data_i:
                        self.levels[i].add(item)

    def print_ct(self):
        print 'root: ', self.ct.data
        self.ct.prettyTree()
        for level in self.levels:
            print [i.data for i in level]

    def clustering_from_ct(self, k):
        levels_counts = [len(i) for i in self.levels]
        if k <= 0:
            print "Invalid k!"
            return
        elif k == 1:
            return [[i.data for i in self.levels[np.argmax(levels_counts)]]]
        else:
            for i, count in enumerate(levels_counts):
                if count >= k:
                    centroids = self.levels[i]
                    break
            return self._clustering_from_centroids(centroids, k)

    def _clustering_from_centroids(self, centroids, k):

        centroids = list(centroids)

        def find_all_sub_childrens(tree):
            data_list = set()

            def _rec(tree):
                data_list.add(tree.data)
                children = tree.getChildren()
                if children:
                    for child in children:
                        data_list.add(child.data)
                        _rec(child)
                return data_list
            return _rec(tree)

        clusters = [find_all_sub_childrens(i) for i in centroids]

        no_clusters_to_delete = len(clusters) - k
        while no_clusters_to_delete > 0:
            num = min(2 * no_clusters_to_delete, len(clusters))
            clusters_merged_index = random.sample(range(len(clusters)), num)
            num = len(clusters_merged_index) / 2
            if len(clusters_merged_index) % 2 != 0:
                del clusters_merged_index[-1]
            for i in range(num):
                clusters[clusters_merged_index[i]] = clusters[clusters_merged_index[i]] | clusters[clusters_merged_index[i + num]]

            clusters_merged_index = sorted(clusters_merged_index[num:])
            for offset, index in enumerate(clusters_merged_index):
                index -= offset
                del clusters[index]
                del centroids[index]
            no_clusters_to_delete = len(clusters) - k

        centroids = [i.data for i in centroids]
        return centroids, clusters


class DM_GReader():

    def __init__(self, username, password, method='kmeans'):
        auth = ClientAuthMethod(username, password)
        self.reader = GoogleReader(auth)
        self.reader.buildSubscriptionList()
        self.categories = self.reader.getCategories()
        self.corpus = Corpus()
        self.method = method

    def import_category(self, category_id=0, path=None, local=False, max_articles=2000, days=3):
        """Import the specific category to a Pattern Corpus for future calculation.
        category_id: the integer indicates which category to use.
        cont: the integer tells how many queries to issue to continuously crawl the GReader.
        path: the location for storing the pickle of the Pattern Corpus.
        local: to use the local stored corpus?
        max_articles: the number of max articles we try to crawl if one day's subscriptions is too much."""

        if path is None:
            print "Please provide with a path to store/load local pickle file."
            return

        if local:
            self.corpus = Corpus.load(path)
            return

        self.target_category = self.categories[category_id]
        continuation = None

        # Crawl only the data within one day
        time_threadshold = calendar.timegm((datetime.date.today() - datetime.timedelta(days=days)).timetuple())

        i = 1

        while 1 and i < (max_articles / 20):

            self.target_category_content = self.reader.getCategoryContent(self.target_category, continuation=continuation)
            feeds = self.target_category_content[u'items']

            if self.target_category_content['updated'] < time_threadshold:
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

            print 'Retrieving %d articles...' % (i * 20)
            i = i + 1

        self.corpus.save(path, update=True)

    def _generate_clusters(self, k=10, p=0.8, maxlevel=10):
        """Use KMEANS method by default, and choose the initial k values by KMPP method.
        k is the number of clusters.
        p is to control the error of KMEANS, when p=1.0 is faster with small error.
        """
        if self.method == "kmeans":

            from pattern.vector import KMEANS, KMPP
            self.clusters = self.corpus.cluster(method=KMEANS, k=k, seed=KMPP, p=p, iterations=10)
            doc_list = []
            # For each cluster, calculate the centroid, and calculate the doc (vector) which is nearest to the centroid.
            for cluster in self.clusters:
                c = centroid(cluster)
                d_min = (cluster[0].vector, c)
                for doc in cluster:
                    d = distance(doc.vector, c)
                    if distance(doc.vector, c) < d_min:
                        d_min = d
                        doc_min = doc
                doc_list.append(doc_min)
            self.centroids = [i.name for i in doc_list]
            self.clusters = [[i.name for i in cluster] for cluster in self.clusters]

        elif self.method == 'covertree':

            def mydistance(doc_name1, doc_name2):
                v1 = self.corpus.document(doc_name1).vector
                v2 = self.corpus.document(doc_name2).vector
                return distance(v1, v2)

            self.covertree = Covertree(mydistance, maxlevel)

            for i, doc in enumerate(self.corpus):
                tree_node = myTree(doc.name)
                self.covertree.insert(tree_node, self.covertree.ct, 0)

            self.covertree.merge_levels()
            self.centroids, self.clusters = self.covertree.clustering_from_ct(k)

    def generate_repr_ids(self, k):
        """
        For each cluster, we choose an arbitary article as the cluster's representative.

        Return the ids of the article, here the document name is the article's id.
        Google Reader is using "i=http://www.google.com/reader/api/0/stream/items/contents" to get the content of a specific data.
        Now we use the centroid to represent the documents

        """
        self._generate_clusters(k)
        return self.centroids

    def cost(self):
        cost = 0
        for i, center in enumerate(self.centroids):
            for doc in self.clusters[i]:
                cost += distance(self.corpus.document(doc).vector, self.corpus.document(center).vector)

        return cost

    def get_article_content(self, ids):
        """
        Use the ids to find the content of the articles through google web content API
        """
        url = 'http://www.google.com/reader/api/0/stream/items/contents'
        id_handle = 'tag:google.com,2005:reader/item/%s'

        contents = []
        for _id in ids:
            r = requests.post(url, data={'i': (id_handle % _id)})
            contents.append(r.json)
        return contents

    def generate_htmls(self, k, ids):
        """
        Use the ids and k to generate htmls
        """
        htmls = {}
        for i in self.get_article_content(ids):
            feed = i['items'][0]
            for content in [u'content', u'summary']:
                if content in feed:
                    title = feed['title']
                    url = feed['alternate'][0]['href']
                    htmls[title] = url
        return htmls
