Introduction
==========
DM GReader is a data mining tool built upon personal Google Reader. It is motivated by my overwhelming 1000+ per day new unread articles in Google Reader. DM GReader helps me to cluster these articles into k groups using K-Means algorithm, and returns a "Snapshot of Today" list, which contains k articles from k clusters. Intuitively, it gives me a broad but representative view of the new feeds.

Features
==========
* To generate a "snapshot" like feature of one day's summary.
* To cluster one day's feeds into k groups, focus on users' interests.
* TODO:
    * Other ways to generate the articles that is interesting to the user.
    * Implement a web interface.
    * Implement a database for storing one users' data. Cache the "Snapshot of Today" articles.
    * Implement a mobile web interface.

Version
==========
0.0.1


Usage
==========
Example:

```python
import DM_GReader
import pprint
pp = pprint.PrettyPrinter(indent=4)

Username = 'foobar@gmail.com'
Password = 'password'

dm = DM_GReader.DM_GReader(Username, Password)
dm.import_category(local=True, path='path')

# Generate Representative Articles
# Given k, e.g. here k=10
#     Generate the most representative 10 articles 
#     within one day of the Google Reader subscription.
ids = dm.generate_repr_ids(10)
pp.pprint([i['items'][0]['title'] \
    for i in dm.get_article_content(ids)]) # Print these 10 articles' title

# Generate Latent space analysis(LSA) over the whole corpus.
dm.corpus.lsa = None
dm.corpus.reduce(300) # reduce the vocalbulary to 300 concepts(topics)
# generate the representative sample articles again
ids = dm.generate_repr_ids(10)
pp.pprint([i['items'][0]['title'] for i in dm.get_article_content(ids)]) 
```

This will import the remote Google Reader data and dump it to local pickle data for future use.

Sample Output. We compared both the original and latent space analysis (LSA) results below.

<pre>

'k=10, Origianl'
[   u'Meet a NetBeans Contributor: Benno Markiewicz',
    u'INFOGRAPHIC The Evolution of Windows OS From Beginning to Present',
    u'How to calculate Compound Interest in Java ?',
    u'Running maven commands with multi modules project',
    u'Foursquare Explore Is Now A Search Tool Anyone Can Use, No Check-Ins Required',
    u'Microsoft To Compete Against Spotify With Xbox Music, Available Soon On Xbox, Windows 8, And Windows Phone Devices',
    u'The Joys of Conjugate Priors',
    u'Daily Update for October 15, 2012',
    u'San Francisco Proposes Revised Open Data Legislation, Plans To Hire Chief Data Officer',
    u'Microsoft Betting Big On Surface: Orders 3 To 5 Million Tablets For Q4, Says WSJ']

'k=20, Origianl'
[   u'How Can I Recover Data from a Dead or Erased Hard Drive? [Ask Lifehacker]',
    u'The Joys of Conjugate Priors',
    u'INFOGRAPHIC The Evolution of Windows OS From Beginning to Present',
    u'LG Optimus G brings 13 megapixels of shooting prowess to Sprint on November 11th for $200',
    u'11 Simple Ways to Create Genuine Connections with the People Who Make Failure Impossible',
    u'Windows Store App Development Snack: Feedback Links in Your App',
    u'Meet The New Foursquare, The One That You\u2019ve Helped Build And Continue To Power',
    u'Combining Edge Animate and CSS FilterLab (video)',
    u'iPhone appealing as BYOD smartphone thanks to security warning',
    u"Apple snags Amazon's A9 head to lead Siri team",
    u'Linux 3.7-rc1 Kernel Released With Many Features',
    u'How to calculate Compound Interest in Java ?',
    u'Programming udp sockets in python',
    u'Teapots and Detergent Bottles Transformed Into Glitchy Works Of Art',
    u'Apple Rumor Patrol: The Truth About The Long-Promised iPad Mini',
    u'How to Run a Compute-Intensive Task in Java on a Virtual Machine',
    u'Reporting with Django Multi-DB Support',
    u'DailyJS: Node Roundup: otr, matches.js, mariasql',
    u'Use Sex Pills To Prolong Your Intercourse',
    u'Meet a NetBeans Contributor: Benno Markiewicz']

'k=10, LSA'
[   u'Delegates and Multicast Delegates with example code in C# and VB',
    u'While You Were Sleeping: Sprint Announces \u201cSpecial Webcast\u201d For 4am Eastern Today; $20B Softbank Investment Confirmed?',
    u'The Joys of Conjugate Priors',
    u'A new kind of fractal?',
    u'Microsoft announces Xbox Music',
    u"Rumor Roundup: The 'Yep' heard 'round the world",
    u'How to hide taskbar or show taskbar using vb.net',
    u'Microsoft Surface for Windows RT pricing now official: tablet starts at $499, keyboard not included',
    u'My top 5 Scala articles selection for week 08-14 October',
    u'Programming udp sockets in python']

'k=20, LSA'
[   u'News: Linux Top 3: UEFI Secure Boot, Amazon AMI and Ubuntu 12.10 Donations',
    u'Programming udp sockets in python',
    u'Meet a NetBeans Contributor: Benno Markiewicz',
    u'Facebook Offers Are A Viral Hit: Friend-To-Friend Sharing Drives 3/4s Of Popular Coupon Redemptions',
    u'Mageia 3 Gets Its Second Alpha Release',
    u'Google tests searches that include Calendar, Drive in results',
    u"Rumor Roundup: The 'Yep' heard 'round the world",
    u'The Joys of Conjugate Priors',
    u'Understanding Dependency Inversion in real life',
    u'Leaked screenshots hint at Google Maps for iOS 6',
    u'Teapots and Detergent Bottles Transformed Into Glitchy Works Of Art',
    u'Microsoft Surface for Windows RT pricing now official: tablet starts at $499, keyboard not included',
    u'When, if ever, will your LG smartphone get Android 4.1?',
    u'[Statistics] Probability Question',
    u"I'm reclining my seat on the airplane. Deal with it. [Discussions Of The Day]",
    u'A new kind of fractal?',
    u'Foxconn admits hiring underage interns',
    u'Windows Store App Development Snack: Feedback Links in Your App',
    u'ASP.NET: Register HttpModule at runtime | dotnetExpertGuide.com',
    u"Microsoft's Xbox Music to challenge iTunes, others"]

</pre>

The results of clustering approximate 800 articles (mainly the latest one day subscriptions), for both Original and LSA. One can see that after reducing the corpus to 300 concepts/topics, it significantly shorten the running time.

|Running time (s)|k=10|k=20|
|:-------|:-----:|:-----:|
|Original|97.599|68.585|
|LSA|17.390|27.693|

Credits
==========
This Python package is built upon [libgreader](https://github.com/askedrelic/libgreader) and [pattern](https://github.com/clips/pattern).
