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

Sample Output
-------------
<pre>
# Snapshot of today's articles. (k=10)
[   u'JDBC Connectivity with Mysql in Java',
    u'Epic Sculptures Made From Old VHS Tapes',
    u'Remains of the Day: Control issues',
    u"Kickstarting: A Modern Take On The Classic Miner's Lamp",
    u'Google+ Mobile Apps Now Support Pages, iOS App Gets iPhone 5 Support And Finally Lets You Edit Your Posts',
    u"MathML is now enabled in webkit, so MathML rendering in major browsers is on it's way in the near future!",
    u'Samsung announces Galaxy S III mini: 4-inch Super AMOLED display, 1GHz dual-core CPU, NFC',
    u'Firefox Debuts New Developer Toolbar',
    u'Sony Is Your Own Personal "Q" In New "Skyfall" Game',
    u"Apple's bouncy new iPod TV ad"]

# Snapshot of today's articles. (k=20)
[   u"Kickstarting: A Modern Take On The Classic Miner's Lamp",
    u'Buy Tuxedos and Cashmere Used (Because Newer Is Not Better) [Clothing]',
    u'Epic Sculptures Made From Old VHS Tapes',
    u'How to Stop a Soda Can From Fizzing Over [Video]',
    u'How to Plot 911 Police &amp; Fire Responses in R',
    u'The Cooking Methods Cheat Sheet Clears Up All Those Confusing Cooking Terms [Infographics]',
    u"Remains of the Day: Mozilla Pulls Firefox 16 Due to Security Vulnerability [For What It's Worth]",
    u'Two of My Favorite Javascript Design Patterns',
    u"Ban on Samsung's Galaxy Nexus overturned by U.S. appeals court",
    u'Infographic: The Cost Of A Famous Logo? From $0 To $211 Million',
    u'World-Class Buildings For The Underserved, At Under $10k',
    u"Electric Cars Aren't The Future Of Car Sharing--Yet",
    u'Construct BST from given preorder traversal | Set 1',
    u'Scalable cheap DIY Wordpress hosting',
    u'Canonical Work to Improve Gaming on Ubuntu',
    u'An Intuitive Guide to Linear Algebra',
    u"Mathematicians Extend Einstein's Special Relativity Beyond Speed of Light - Slashdot",
    u'EnumMap vs HashMap in Java',
    u'JDBC Connectivity with Mysql in Java',
    u'What OAuth Lacks: Resource Owner Initiated OAuth Delegation']
</pre>

Credits
==========

This Python package is built upon libgreader and pattern.
