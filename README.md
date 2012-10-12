Data mining tools built upon personal Google Reader
==========

* To generate a "snapshot" like feature of one day's summary.
* To cluster one day's feeds into k groups, focus on users' interests.
* To score the importance of the articles, detect duplication, similarity calculation and other typical data mining tools.



Usage
==========

Example:

    import DM_GReader
    import pprint
    pp = pprint.PrettyPrinter(indent=4)

    Username = 'foobar@gmail.com'
    Password = 'password'

    dm = DM_GReader.DM_GReader(Username, Password)
    dm.import_category(local=True, path='path')

    # Generate Representative Articles
    # Given k, e.g. here k=10, generate the most representative 10 articles within one day of the Google Reader subscription.
    ids = dm.generate_repr_ids(10)
    pp.pprint([i['items'][0]['title'] for i in dm.get_article_content(ids)]) # Print these 10 articles' title

    # Generate Latent space analysis(LSA) over the whole corpus.
    dm.corpus.lsa = None
    dm.corpus.reduce(100)

    for word, weight in dm.corpus.lsa.concepts[1].items():
        if abs(weight) > 0.1:
            print word


This will import the remote Google Reader data and dump it to local pickle data for future use.



Credits
==========

This Python package is built upon libgreader and pattern.
